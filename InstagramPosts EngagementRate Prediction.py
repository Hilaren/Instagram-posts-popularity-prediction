# -*- coding: utf-8 -*-
"""00_Hila_Assignment_IG_user-engage-analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SrqhGwn7BPa0STX7C3B0sL7gvVSAZCvi
"""

# Mount GoogleDrive

!pip install -Uqq fastbook
import fastbook
fastbook.setup_book()

# Import Library

from fastbook import *
from fastai.vision.widgets import *

from pathlib import Path

from google.colab import drive
import shutil

path = Path("/content/gdrive/MyDrive/Colab Notebooks/unpack AI 2021/sezane/Sezane_IM_Classification")

path.ls()

# make a list of all images of low
list_low = [f for f in (path / "Low").iterdir() if f.is_file()]
list_low

# pick one and show it
picked_image = 0

im = Image.open(list_low[picked_image])
im.to_thumb(128,128)

# use different data augmentation methods

sezane_imgs = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(128)
)

dls = sezane_imgs.dataloaders(path)
dls.valid.show_batch(max_n=6, nrows=1)

sezane_imgs = sezane_imgs.new(item_tfms=Resize(128, ResizeMethod.Squish))
dls = sezane_imgs.dataloaders(path)
dls.valid.show_batch(max_n=6, nrows=1)

sezane_imgs = sezane_imgs.new(item_tfms=Resize(128, ResizeMethod.Pad, pad_mode="zeros"))
dls = sezane_imgs.dataloaders(path)
dls.valid.show_batch(max_n=6, nrows=1)

sezane_imgs = sezane_imgs.new(item_tfms=RandomResizedCrop(128, min_scale=0.3))
dls = sezane_imgs.dataloaders(path)
dls.valid.show_batch(max_n=6, nrows=1, unique=True)

sezane_imgs = sezane_imgs.new(item_tfms=Resize(128), batch_tfms=aug_transforms(mult=2))
dls = sezane_imgs.dataloaders(path)
dls.valid.show_batch(max_n=12, nrows=2, unique=True)

# Train the Model

sezane_imgs = sezane_imgs.new(
    item_tfms=RandomResizedCrop(224, min_scale=0.5),
    batch_tfms = aug_transforms(mult=2)
)
dls = sezane_imgs.dataloaders(path)

fns = get_image_files(path)
fns

learn = cnn_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(2)

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

interp.plot_top_losses(5, nrows=1)

# Create an App

btn_upload = widgets.FileUpload()
btn_upload

img = PILImage.create(btn_upload.data[-1])
img

out_pl = widgets.Output()
out_pl.clear_output()
with out_pl: display(img.to_thumb(128, 128))
out_pl

pred, pred_idx, probs = learn.predict(img)

lbl_pred = widgets.Label()
lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
lbl_pred