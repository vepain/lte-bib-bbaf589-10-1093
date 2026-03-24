#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Versus figures for uniqify ground truths.
# ------------------------------------------------------------------------------------ #
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

exp_dir=experiments/one_bin/gt_vs_gt

measures="unw_comp unw_hom w_comp w_hom"

x_evals_tsv=$exp_dir/evals/with_chromosomes.tsv
x_label="With chromosomes"

y_evals_tsv=$exp_dir/evals/only_plasmids.tsv
y_label="Only plasmids"

figs_dir="$exp_dir/figs"

for measure in $measures; do
    fig_pdf="$figs_dir/$measure.pdf"
    lteu figs vs gt "$measure" "$fig_pdf" \
        --x-axis "$x_evals_tsv" --x-label "$x_label" \
        --y-axis "$y_evals_tsv" --y-label "$y_label" \
        --context "$context" "$focus_mode"
done
