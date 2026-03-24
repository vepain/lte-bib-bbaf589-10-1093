#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Create the distributions figure for experiment one bin binning.
# ------------------------------------------------------------------------------------ #
tools="hyasp mob gplas2"
rm_samples_mode="fails" # | nothing
#
# Figures aesthetics
#
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

exp_dir="experiments/one_bin/binning"

only_plm_tools_evals_tsv="$exp_dir/evals/only_plasmids/merge.tsv"
with_chm_tools_evals_tsv="$exp_dir/evals/with_chromosomes/merge.tsv"

fig_pdf="$exp_dir/figs/distributions_no_pbf.pdf"

sopt_tools=()
for tool in $tools; do
    sopt_tools+=(--tool "$tool")
done

lteu figs dist tools \
    "$only_plm_tools_evals_tsv" "$with_chm_tools_evals_tsv" "$fig_pdf" \
    "${sopt_tools[@]}" \
    --remove-samples "$rm_samples_mode" \
    --context "$context" "$focus_mode"
