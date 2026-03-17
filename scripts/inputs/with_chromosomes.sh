#!/usr/bin/env bash

tools="hyasp mob pbf gplas2"
declare -r content="with_chromosomes"

for tool in $tools; do
    lteu fmt bins original/predictions.xlsx "$tool" "binning/$content/$tool" --with-chromosomes
done
