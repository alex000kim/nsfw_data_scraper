# NSFW Data Scraper

## Note: use with caution - the dataset is noisy

## Description

This is a set of scripts that allows for an automatic collection of _tens of thousands_ of images for the following (loosely defined) categories to be later used for training an image classifier:
- `porn` - pornography images
- `hentai` - hentai images, but also includes pornographic drawings
- `sexy` - sexually explicit images, but not pornography. Think nude photos, playboy, bikini, etc.
- `neutral` - safe for work neutral images of everyday things and people
- `drawings` - safe for work drawings (including anime)

Here is what each script (located under `scripts` directory) does:
- `1_get_urls_.sh` - iterates through text files under `scripts/source_urls` downloading URLs of images for each of the 5 categories above. The [Ripme](https://github.com/RipMeApp/ripme) application performs all the heavy lifting. The source URLs are mostly links to various subreddits, but could be any website that Ripme supports.
*Note*: I already ran this script for you, and its outputs are located in `raw_data` directory. No need to rerun unless you edit files under `scripts/source_urls`.
- `2_download_from_urls_.sh` - downloads actual images for urls found in text files in `raw_data` directory.
- `3_optional_download_drawings_.sh` - (optional) script that downloads SFW anime images from the [Danbooru2018](https://www.gwern.net/Danbooru2018) database.
- `4_optional_download_neutral_.sh` - (optional) script that downloads SFW neutral images from the [Caltech256](http://www.vision.caltech.edu/Image_Datasets/Caltech256/) dataset
- `5_create_train_.sh` - creates `data/train` directory and copy all `*.jpg` and `*.jpeg` files into it from `raw_data`. Also removes corrupted images.
- `6_create_test_.sh` - creates `data/test` directory and moves `N=2000` random files for each class from `data/train` to `data/test` (change this number inside the script if you need a different train/test split). Alternatively, you can run it multiple times, each time it will move `N` images for each class from `data/train` to `data/test`.

## Prerequisites

- Docker

## How to collect data

```bash
$ docker build . -t docker_nsfw_data_scraper
Sending build context to Docker daemon  426.3MB
Step 1/3 : FROM ubuntu:18.04
 ---> 775349758637
Step 2/3 : RUN apt update  && apt upgrade -y  && apt install wget rsync imagemagick default-jre -y
 ---> Using cache
 ---> b2129908e7e2
Step 3/3 : ENTRYPOINT ["/bin/bash"]
 ---> Using cache
 ---> d32c5ae5235b
Successfully built d32c5ae5235b
Successfully tagged docker_nsfw_data_scraper:latest
$ # Next command might run for several hours. It is recommended to leave it overnight
$ docker run -v $(pwd):/root/nsfw_data_scraper docker_nsfw_data_scraper scripts/runall.sh
Getting images for class: neutral
...
...
$ ls data
test  train
$ ls data/train/
drawings  hentai  neutral  porn  sexy
$ ls data/test/
drawings  hentai  neutral  porn  sexy
```

## How to train a CNN model
- Install [fastai](https://github.com/fastai/fastai): `conda install -c pytorch -c fastai fastai`
- Run `train_model.ipynb` top to bottom

## Results

I was able to train a CNN classifier to 91% accuracy with the following confusion matrix:
![alt text](confusion_matrix.png)

As expected,  `drawings` and `hentai` are confused with each other more frequently than with other classes.

Same with `porn` and `sexy` categories.

