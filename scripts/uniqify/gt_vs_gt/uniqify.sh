#!/usr/bin/env bash

exp_dir=experiments/uniqify/gt_vs_gt

uv run lteu uniqify gt ground_truths/only_plasmids "$exp_dir/samples.tsv" "$exp_dir/ground_truths"
