#!/usr/bin/env bash

exp_dir=experiments/overview

contents="only_plasmids with_chromosomes"

for content in $contents; do

    eval_dir="$exp_dir/evals/$content"

    lteu eval merge \
        -t hyasp -i "$eval_dir/hyasp.tsv" \
        -t mob -i "$eval_dir/mob.tsv" \
        -t pbf -i "$eval_dir/pbf.tsv" \
        -t gplas2 -i "$eval_dir/gplas2.tsv" \
        "$eval_dir/merge.tsv"
done
