#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Distribution figure for one bin.
# ------------------------------------------------------------------------------------ #
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

exp_dir=experiments/one_bin

only_plm_eval_tsv=$exp_dir/evals/only_plasmids.tsv
with_chm_eval_tsv=$exp_dir/evals/with_chromosomes.tsv

fig_pdf="$exp_dir/figs/distribution.pdf"

uv run lteu figs dist gt \
    "$only_plm_eval_tsv" "$with_chm_eval_tsv" "$fig_pdf" \
    --context "$context" "$focus_mode"
