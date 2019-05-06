#!/bin/bash

scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
base_dir="$(dirname "$scripts_dir")"
raw_data_dir="$base_dir/raw_data"
data_dir="$base_dir/data"

declare -a class_names=(
	"neutral"
	"drawings"
	"sexy"
	"porn"
	"hentai"
	)

train_dir="$data_dir/train"
mkdir -p "$train_dir"

echo "Copying image to the training folder"
for cname in "${class_names[@]}"
do
	raw_data_class_dir="$raw_data_dir/$cname"
	if [[ -d "$raw_data_class_dir" ]]
	then
		mkdir -p "$train_dir/$cname"
		find "$raw_data_class_dir" -type f \( -name '*.jpg' -o -name '*.jpeg' \) -print0 |
		while IFS= read -r -d '' jpg_f
		do
		    cp "$jpg_f" "$train_dir/$cname/$(uuidgen).jpg"
		done
	fi
done

echo "Removing corrupted images"
find "$train_dir" -type f -name '*.jpg' -print0 | 
while IFS= read -r -d '' jpg_f
do
    is_corrupted="$(convert "$jpg_f" /dev/null &> /dev/null; echo $?)"
	if [[ "$is_corrupted" -eq  "1" ]] || [ `identify "$jpg_f" | wc -l` -gt 1 ]
	then
		echo "removing: $jpg_f"
		rm "$jpg_f"
	fi
done

echo "Number of files per class:"
for subdir in $(ls "$train_dir")
do 
	echo "$subdir": "$(find "$train_dir/$subdir" -type f | wc -l)"
done
