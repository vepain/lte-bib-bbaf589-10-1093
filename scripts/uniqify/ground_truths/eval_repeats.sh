#!/usr/bin/env bash

contents="only_plasmids with_chromosomes"

for content in $contents; do
    gt_dir=ground_truths/$content
    uv run lteu eval run "$gt_dir" "$gt_dir" "samples/repeats/$content.tsv" "comp_hom/$content/repeats/ground_truths.tsv"
done
