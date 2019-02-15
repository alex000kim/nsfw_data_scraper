#!/bin/bash

scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
base_dir="$(dirname "$scripts_dir")"
raw_data_dir="$base_dir/raw_data"

declare -a class_names=(
	"neutral"
	"drawings"
	"sexy"
	"porn"
	"hentai"
	)

for cname in "${class_names[@]}"
do
	urls_file="$raw_data_dir/$cname/urls_$cname.txt"
	images_dir="$raw_data_dir/$cname/IMAGES"
	mkdir -p "$images_dir"
	echo "Class: $cname. Total # of urls: $(cat $urls_file | wc -l)"
	echo "Downloading images..."
	xargs -n 20 -P 8 wget -nc -q --timeout=5 --tries=2 -P "$images_dir" < "$urls_file"
done
