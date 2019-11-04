#!/bin/bash

scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
base_dir="$(dirname "$scripts_dir")"
raw_data_dir="$base_dir/raw_data"
mkdir -p "$raw_data_dir/neutral"

wget http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar -P "$raw_data_dir/neutral"
tar -xf "$raw_data_dir/neutral/256_ObjectCategories.tar" -C "$raw_data_dir/neutral"
