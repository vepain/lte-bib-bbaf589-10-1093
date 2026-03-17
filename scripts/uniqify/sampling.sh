#!/usr/bin/env bash

contents="only_plasmids with_chromosomes"

for content in $contents; do
    uv run lteu smp repeats samples/complete_hybrid_asm.tsv "ground_truths/$content" "samples/repeats/$content.tsv"
done
