#!/usr/bin/env bash

exp_dir=experiments/uniqify/gt_vs_gt

contents="only_plasmids with_chromosomes"

for content in $contents; do
    gt_dir=ground_truths/$content
    uv run lteu eval run "$gt_dir" "$gt_dir" "$exp_dir/samples.tsv" "$exp_dir/evals/$content/original.tsv"
done
