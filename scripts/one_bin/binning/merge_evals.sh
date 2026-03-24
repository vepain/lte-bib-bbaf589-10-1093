#!/usr/bin/env bash

exp_dir="experiments/one_bin/binning"

contents="only_plasmids with_chromosomes"

tools="hyasp mob pbf gplas2"

for content in $contents; do

    sopt_tools=()
    for tool in $tools; do
        sopt_tools+=(--tool-code "$tool")
        sopt_tools+=(--eval-tsv "$exp_dir/evals/$content/$tool.tsv")
    done

    lteu eval merge \
        "${sopt_tools[@]}" \
        "$exp_dir/evals/$content/merge.tsv"
done
