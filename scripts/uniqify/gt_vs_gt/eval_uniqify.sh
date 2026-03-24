#!/usr/bin/env bash

exp_dir=experiments/uniqify/gt_vs_gt

contents="only_plasmids with_chromosomes"

for content in $contents; do
    gt_dir=$exp_dir/ground_truths/$content
    lteu eval run "$gt_dir" "$gt_dir" "$exp_dir/samples.tsv" "$exp_dir/evals/$content/uniqify.tsv"
done
