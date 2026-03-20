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

sopt_tools=()
for str in $tools; do
    sopt_tools+=(--tool "$str")
done

measure_modes="Unweighted Weighted"

for measure_mode in $measure_modes; do
    fig_pdf="$exp_dir/figs/distributions_content_$measure_mode.pdf"

    uv run lteu figs dist tools-content \
        "$only_plm_tools_evals_tsv" "$with_chm_tools_evals_tsv" "$measure_mode" "$fig_pdf" \
        "${sopt_tools[@]}" \
        --remove-samples "$rm_samples_mode" \
        --context "$context" "$focus_mode"
done
