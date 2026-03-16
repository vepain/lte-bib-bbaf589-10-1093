#!/usr/bin/env bash

contents="only_plasmids with_chromosomes"

for content in $contents; do
    uv run lteu uniqify gt "ground_truths/$content" samples/complete_hybrid_asm.tsv "uniqify/$content/ground_truths"
done
