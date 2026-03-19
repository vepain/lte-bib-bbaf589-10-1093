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

exp_dir=experiments/chromosomes

only_plm_tools_evals_tsv=$exp_dir/only_plasmids/evals/merge.tsv
with_chm_tools_evals_tsv=$exp_dir/with_chromosomes/evals/merge.tsv

fig_pdf="$exp_dir/figs/distribution.pdf"

sopt_meths=()
for str in $tools; do
    sopt_meths+=(--tool "$str")
done

uv run lteu figs dist tools \
    "$only_plm_tools_evals_tsv" "$with_chm_tools_evals_tsv" "$fig_pdf" \
    "${sopt_meths[@]}" \
    --remove-samples "$rm_samples_mode" \
    --context "$context" "$focus_mode"
