#!/usr/bin/env bash

exp_dir=experiments/uniqify/ground_truths

contents="only_plasmids with_chromosomes"

for content in $contents; do
    uv run lteu smp repeats samples/complete_hybrid_asm.tsv "ground_truths/$content" "$exp_dir/$content/samples.tsv"
done
