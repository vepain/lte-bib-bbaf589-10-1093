#!/usr/bin/env bash

tools="hyasp mob pbf gplas2"

#
# Predicted plasmid bins
#
content=only_plasmids
for tool in $tools; do
    lteu fmt bins original/predictions.xlsx "$tool" "binning/$content/$tool"
done

#
# Predicted plasmid bins + chromosomal bin (remaining contigs)
#
content=with_chromosomes
for tool in $tools; do
    lteu fmt bins original/predictions.xlsx "$tool" "binning/$content/$tool" --with-chromosomes
done
