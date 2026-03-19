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

sopt_meths=()
for str in $tools; do
    sopt_meths+=(--tool "$str")
done

contents="only_plasmids with_chromosomes"

for content in $contents; do
    fig_pdf="$exp_dir/figs/distribution_mode_$content.pdf"

    uv run lteu figs dist tools-mode \
        "$only_plm_tools_evals_tsv" "$with_chm_tools_evals_tsv" "$content" "$fig_pdf" \
        "${sopt_meths[@]}" \
        --remove-samples "$rm_samples_mode" \
        --context "$context" "$focus_mode"
done
