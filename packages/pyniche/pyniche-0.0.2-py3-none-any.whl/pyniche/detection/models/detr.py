import os

# torch imports
import torch
from transformers import DetrForObjectDetection, DetrImageProcessor
import lightning as l
from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.loggers import CSVLogger

# local imports
from niche_cv.detection.data.loaders.coco import CocoDetectionDataModule

# external imports
from coco_eval import CocoEvaluator


# Reference:
# https://github.com/NielsRogge/Transformers-Tutorials/blob/master/DETR/Fine_tuning_DetrForObjectDetection_on_custom_dataset_(balloon).ipynb


class Niche_Detr:
    def __init__(self, dir_out, name_task, device, path_model=None):
        """
        Folder structure
        models/
            path to a directory containing outputs of save_pretrained() or HuggingFace model name
        out/
            train/
                <name_task>/
                    weights/
                        best.pt
                    ...
            val/
                <name_task>/
                    results.json
                    ...

        -----
        args
        `path_model`: str
            - pre-trained options: facebook/detr-resnet-50, facebook/detr-resnet-101
            - local path to checkpoints

        """
        # attributes
        self.model = None
        self.dir_val = os.path.join(dir_out, "val")
        self.dir_train = os.path.join(dir_out, "train")
        self.name_task = name_task
        self.device = device
        if path_model is None:
            path_model = "facebook/detr-resnet-50"
        else:
            self.path_model = path_model

    def train(self, path_data, batch=16, epochs=100):
        # prepare dataset
        processor = DetrImageProcessor.from_pretrained(self.path_model)
        data_module, id2label = self.get_data(path_data, processor, batch)

        # configure model
        self.model = Detr(self.path_model, len(id2label))
        dir_out = create_output_dir(self.dir_train, self.name_task)
        callbacks = config_callbacks(dir_out)
        logger = config_loggers(dir_out)

        # setup trainer
        trainer = l.Trainer(
            max_epochs=epochs,
            gradient_clip_val=0.1,
            callbacks=callbacks,
            logger=logger,
        )
        trainer.fit(self.model, data_module)

    def evaluate(self, split="test"):
        self.model = Detr(self.path_model)

    def get_data(self, path_data, processor, batch=16):
        data_module = CocoDetectionDataModule(
            root=path_data, processor=processor, batch_size=batch
        )
        data_module.setup()
        id2label = {k: v["name"] for k, v in data_module.train.coco.cats.items()}
        return data_module, id2label


def create_output_dir(path_out, name_task):
    """
    Create the output directory if it does not exist.
    """
    path_project = os.path.join(path_out, name_task)
    if not os.path.exists(path_project):
        os.makedirs(path_project)

    return path_project


def config_callbacks(dir_out):
    checkpoint_callback = ModelCheckpoint(
        monitor="validation_loss",
        mode="min",
        save_top_k=1,
        verbose=False,
        save_last=False,
        dirpath=dir_out,
        # filename="checkpoint-{val_loss:.6f}",
        filename="model",
    )
    return [checkpoint_callback]


def config_loggers(dir_out):
    csv_logger = CSVLogger(
        save_dir=dir_out,
        name=".",  # won't create a new folder metrics
        version=".",  # won't create a new folder version_x
    )
    return [csv_logger]


class Detr(l.LightningModule):
    """
    https://lightning.ai/docs/pytorch/stable/common/lightning_module.html
    """

    def __init__(
        self, backbone, n_labels=None, lr=1e-4, lr_backbone=1e-5, weight_decay=1e-4
    ):
        """
        backbone: e.g. "facebook/detr-resnet-50"
        n_labels: number of labels
        """
        super().__init__()
        # replace COCO classification head with custom head
        # we specify the "no_timm" variant here to not rely on the timm library
        # for the convolutional backbone
        args = {
            "backbone": backbone,
            "revision": "no_timm",
            "ignore_mismatched_sizes": True,
        }
        if n_labels is not None:
            args["num_labels"] = n_labels
        self.model = DetrForObjectDetection.from_pretrained(**args)

        # see https://github.com/PyTorchLightning/pytorch-lightning/pull/1896
        self.lr = lr
        self.lr_backbone = lr_backbone
        self.weight_decay = weight_decay

    def forward(self, pixel_values, pixel_mask):
        outputs = self.model(pixel_values=pixel_values, pixel_mask=pixel_mask)

        return outputs

    def common_step(self, batch, batch_idx):
        pixel_values = batch["pixel_values"]
        pixel_mask = batch["pixel_mask"]
        labels = [{k: v.to(self.device) for k, v in t.items()} for t in batch["labels"]]

        outputs = self.model(
            pixel_values=pixel_values, pixel_mask=pixel_mask, labels=labels
        )

        loss = outputs.loss
        loss_dict = outputs.loss_dict

        return loss, loss_dict, outputs, labels

    def training_step(self, batch, batch_idx):
        loss, loss_dict, _, _ = self.common_step(batch, batch_idx)
        # logs metrics for each training_step,
        # and the average across the epoch
        self.log("training_loss", loss)
        for k, v in loss_dict.items():
            self.log("train_" + k, v.item())

        return loss

    def validation_step(self, batch, batch_idx):
        loss, loss_dict, _, _ = self.common_step(batch, batch_idx)
        self.log("validation_loss", loss)
        for k, v in loss_dict.items():
            self.log("validation_" + k, v.item())

        return loss

    def test_step(self, batch, batch_idx):
        loss, loss_dict, outputs, labels = self.common_step(batch, batch_idx)

        orig_target_sizes = torch.stack(
            [target["orig_size"] for target in labels], dim=0
        )
        results = self.processor.post_process_object_detection(
            outputs, target_sizes=orig_target_sizes
        )

        predictions = {
            target["image_id"].item(): output for target, output in zip(labels, results)
        }
        predictions = prepare_for_coco_detection(predictions)
        self.evaluator.update(predictions)

    def predict_step(self, batch, batch_idx):
        pass

    def configure_optimizers(self):
        param_dicts = [
            {
                "params": [
                    p
                    for n, p in self.named_parameters()
                    if "backbone" not in n and p.requires_grad
                ]
            },
            {
                "params": [
                    p
                    for n, p in self.named_parameters()
                    if "backbone" in n and p.requires_grad
                ],
                "lr": self.lr_backbone,
            },
        ]
        optimizer = torch.optim.AdamW(
            param_dicts, lr=self.lr, weight_decay=self.weight_decay
        )

        return optimizer


def convert_to_xywh(boxes):
    xmin, ymin, xmax, ymax = boxes.unbind(1)
    return torch.stack((xmin, ymin, xmax - xmin, ymax - ymin), dim=1)


def prepare_for_coco_detection(predictions):
    coco_results = []
    for original_id, prediction in predictions.items():
        if len(prediction) == 0:
            continue

        boxes = prediction["boxes"]
        boxes = convert_to_xywh(boxes).tolist()
        scores = prediction["scores"].tolist()
        labels = prediction["labels"].tolist()

        coco_results.extend(
            [
                {
                    "image_id": original_id,
                    "category_id": labels[k],
                    "bbox": box,
                    "score": scores[k],
                }
                for k, box in enumerate(boxes)
            ]
        )
    return coco_results
