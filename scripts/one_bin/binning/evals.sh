#!/usr/bin/env bash

exp_dir="experiments/one_bin/binning"

contents="only_plasmids with_chromosomes"

tools="hyasp mob pbf gplas2"

for content in $contents; do
    for tool in $tools; do
        lteu eval run "binning/$content/$tool" "ground_truths/$content" "$exp_dir/samples.tsv" "$exp_dir/evals/$content/$tool.tsv"
    done
done
