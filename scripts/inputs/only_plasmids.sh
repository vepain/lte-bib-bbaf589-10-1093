#!/usr/bin/env bash

tools="hyasp mob pbf gplas2"
declare -r content="only_plasmids"

for tool in $tools; do
    lteu fmt bins original/predictions.xlsx "$tool" "binning/$content/$tool"
done
