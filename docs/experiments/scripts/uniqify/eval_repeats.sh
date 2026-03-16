#!/usr/bin/env bash

contents="only_plasmids with_chromosomes"

tools="hyasp mob pbf gplas2"

for content in $contents; do
    for tool in $tools; do
        uv run lteu eval "binning/$content/$tool" "ground_truths/$content" samples/complete_hybrid_asm.tsv "comp_hom/$content/repeats/$tool.tsv"
    done
done
