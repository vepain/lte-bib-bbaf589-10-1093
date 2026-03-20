#!/usr/bin/env bash

exp_dir=experiments/overview

contents="only_plasmids with_chromosomes"

tools="hyasp mob pbf gplas2"

for content in $contents; do
    for tool in $tools; do
        uv run lteu eval run "binning/$content/$tool" "ground_truths/$content" samples/complete_hybrid_asm.tsv "$exp_dir/evals/$content/$tool.tsv"
    done
done
