#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Distribution figure for tools.
# ------------------------------------------------------------------------------------ #
tools="hyasp mob pbf gplas2"
rm_samples_mode="fails" # | nothing
#
# Aesthetics
#
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

exp_dir=experiments/overview

only_plm_tools_evals_tsv=$exp_dir/evals/only_plasmids/merge.tsv
with_chm_tools_evals_tsv=$exp_dir/evals/with_chromosomes/merge.tsv

fig_pdf="$exp_dir/figs/distributions.pdf"

sopt_tools=()
for str in $tools; do
    sopt_tools+=(--tool "$str")
done

uv run lteu figs dist tools \
    "$only_plm_tools_evals_tsv" "$with_chm_tools_evals_tsv" "$fig_pdf" \
    "${sopt_tools[@]}" \
    --remove-samples "$rm_samples_mode" \
    --context "$context" "$focus_mode"
