#!/usr/bin/env bash

exp_dir=experiments/chromosomes

contents="only_plasmids with_chromosomes"

for content in $contents; do
    uv run lteu eval merge \
        -t hyasp -i "$exp_dir/$content/evals/hyasp.tsv" \
        -t mob -i "$exp_dir/$content/evals/mob.tsv" \
        -t pbf -i "$exp_dir/$content/evals/pbf.tsv" \
        -t gplas2 -i "$exp_dir/$content/evals/gplas2.tsv" \
        "$exp_dir/$content/evals/merge.tsv"
done
