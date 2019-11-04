#!/bin/bash

scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
base_dir="$(dirname "$scripts_dir")"
raw_data_dir="$base_dir/raw_data"
drawings_dir="$raw_data_dir/drawings"
download_dir="$drawings_dir/anime_dataset"
mkdir -p "$download_dir"


n_batches=4
# since the numbering starts at 0, actual number of batches will be `n_batches + 1`
# each batch contains roughly 2200 images
for batch_num in $(seq -f "%04g" 0 "$n_batches")
do
    rsync --recursive --times "rsync://78.46.86.149:873/danbooru2018/512px/$batch_num" "$download_dir"
done

# for whatever reason, most images contain black borders
# need to remove them
for subdir_name in $(ls "$download_dir")
do
    find "$download_dir/$subdir_name" -name "*.jpg" -print0 |
    while IFS= read -r -d '' img
    do
        convert "$img" -bordercolor black -border 1x1 -fuzz 20% -trim "$img"
    done
done