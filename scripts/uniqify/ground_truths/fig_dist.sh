#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Distribution figure for uniqify ground truths.
# ------------------------------------------------------------------------------------ #
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

exp_dir=experiments/uniqify/ground_truths

only_plm_eval_tsv=$exp_dir/only_plasmids/evals/repeats.tsv
with_chm_eval_tsv=$exp_dir/with_chromosomes/evals/repeats.tsv

fig_pdf="$exp_dir/figs/distribution.pdf"

uv run lteu figs dist gt \
    "$only_plm_eval_tsv" "$with_chm_eval_tsv" "$fig_pdf" \
    --context "$context" "$focus_mode"
