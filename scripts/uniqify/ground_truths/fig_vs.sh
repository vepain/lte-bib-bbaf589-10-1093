#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Versus figures for uniqify ground truths.
# ------------------------------------------------------------------------------------ #
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

contents="only_plasmids with_chromosomes"
measures="unw_comp unw_hom w_comp w_hom"

figs_dir=figs

for content in $contents; do

    x_evals_tsv=comp_hom/$content/repeats/ground_truths.tsv
    x_label="Original"

    y_evals_tsv=comp_hom/$content/uniqify/ground_truth.tsv
    y_label="Uniqify"

    for measure in $measures; do
        fig_pdf="$figs_dir/uniqify/$content/ground_truths/$measure.pdf"
        uv run lteu figs vs gt "$measure" "$fig_pdf" \
            --x-axis "$x_evals_tsv" --x-label "$x_label" \
            --y-axis "$y_evals_tsv" --y-label "$y_label" \
            --context "$context" "$focus_mode"
    done
done
