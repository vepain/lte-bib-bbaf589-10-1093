#!/usr/bin/env bash

exp_dir=experiments/uniqify/ground_truths

contents="only_plasmids with_chromosomes"

for content in $contents; do
    uv run lteu uniqify gt "ground_truths/$content" "$exp_dir/$content/samples.tsv" "$exp_dir/$content/ground_truths"
done
