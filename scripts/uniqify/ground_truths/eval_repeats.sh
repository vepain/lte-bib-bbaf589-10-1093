#!/usr/bin/env bash

exp_dir=experiments/uniqify/ground_truths

contents="only_plasmids with_chromosomes"

for content in $contents; do
    gt_dir=ground_truths/$content
    uv run lteu eval run "$gt_dir" "$gt_dir" "$exp_dir/$content/samples.tsv" "$exp_dir/$content/evals/repeats.tsv"
done
