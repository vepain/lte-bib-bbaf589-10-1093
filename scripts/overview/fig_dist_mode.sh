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

contents="only_plasmids with_chromosomes"

for content in $contents; do
    fig_pdf="$exp_dir/figs/distributions_mode_$content.pdf"

    lteu figs dist tools-mode \
        "$only_plm_tools_evals_tsv" "$with_chm_tools_evals_tsv" "$content" "$fig_pdf" \
        "${sopt_tools[@]}" \
        --remove-samples "$rm_samples_mode" \
        --context "$context" "$focus_mode"
done
