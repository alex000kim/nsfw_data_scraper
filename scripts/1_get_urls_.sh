#!/bin/bash

scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source_urls_dirname="source_urls"

if [[ "$1" == "test" ]]
then
	echo "Running in test mode" 
	source_urls_dirname="source_urls_test"
fi

base_dir="$(dirname "$scripts_dir")"
raw_data_dir="$base_dir/raw_data"

declare -a class_names=(
	"neutral"
	"drawings"
	"sexy"
	"porn"
	"hentai"
	)

#download ripme.jar
wget https://github.com/RipMeApp/ripme/releases/download/1.7.95/ripme.jar -O $scripts_dir/ripme.jar

for cname in "${class_names[@]}"
do
	echo "--- Getting images for class: $cname"
	
	while read url
	do
		echo "------ url: $url"
		if [[ ! "$url" =~ ^"#" ]]
		then
			echo "$url"
			java -jar "$scripts_dir/ripme.jar" --skip404 --no-prop-file --ripsdirectory "$raw_data_dir/$cname" --url "$url"
		fi
	done < "$scripts_dir/$source_urls_dirname/$cname.txt"
done

for cname in "${class_names[@]}"
do
	urls_file="$raw_data_dir/$cname/urls_$cname.txt"
	tmpfile=$(mktemp)
	find "$raw_data_dir/$cname" -type f -name "urls.txt" -exec cat {} + >> "$tmpfile"
	grep -e ".jpeg" -e ".jpg" "$tmpfile" > "$urls_file"
	sort -u -o "$urls_file" "$urls_file"
	rm "$tmpfile"
done