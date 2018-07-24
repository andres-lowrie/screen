#!/bin/sh

PER_PAGE=100

mkdir data
cd data
repos=$(curl -s https://api.github.com/orgs/datasets/repos?per_page=$PER_PAGE | jq -r '.[].clone_url')
for repo in $repos; do
	git clone $repo;
done

find . -type f -name '*.csv' > csv_files.txt