#!/usr/bin/env bash

contents="only_plasmids with_chromosomes"

for content in $contents; do
    gt_dir=uniqify/$content/ground_truths
    uv run lteu eval run "$gt_dir" "$gt_dir" "samples/repeats/$content.tsv" "comp_hom/$content/uniqify/ground_truth.tsv"
done
