#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Versus figures for uniqify ground truths.
# ------------------------------------------------------------------------------------ #
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

exp_dir=experiments/uniqify/ground_truths

contents="only_plasmids with_chromosomes"
measures="unw_comp unw_hom w_comp w_hom"

for content in $contents; do

    x_evals_tsv=$exp_dir/$content/evals/repeats.tsv
    x_label="Original"

    y_evals_tsv=$exp_dir/$content/evals/uniqify.tsv
    y_label="Uniqify"

    figs_dir="$exp_dir/$content/figs"

    for measure in $measures; do
        fig_pdf="$figs_dir/$measure.pdf"
        uv run lteu figs uniqify gt vs "$measure" "$fig_pdf" \
            --x-axis "$x_evals_tsv" --x-label "$x_label" \
            --y-axis "$y_evals_tsv" --y-label "$y_label" \
            --context "$context" "$focus_mode"
    done
done
