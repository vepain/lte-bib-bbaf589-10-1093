#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Distribution figure for uniqify gt versus gt.
# ------------------------------------------------------------------------------------ #
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

exp_dir=experiments/uniqify/gt_vs_gt

only_plm_eval_tsv=$exp_dir/evals/only_plasmids/original.tsv
with_chm_eval_tsv=$exp_dir/evals/with_chromosomes/original.tsv

fig_pdf="$exp_dir/figs/distributions.pdf"

lteu figs dist gt \
    "$only_plm_eval_tsv" "$with_chm_eval_tsv" "$fig_pdf" \
    --context "$context" "$focus_mode"
