#!/usr/bin/env bash

exp_dir=experiments/uniqify/gt_vs_gt

contents="only_plasmids with_chromosomes"

for content in $contents; do
    lteu uniqify gt "ground_truths/$content" "$exp_dir/samples.tsv" "$exp_dir/ground_truths/$content"
done
