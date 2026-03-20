#!/usr/bin/env bash

exp_dir=experiments/uniqify/gt_vs_gt

lteu smp repeats samples/complete_hybrid_asm.tsv ground_truths/only_plasmids "$exp_dir/samples.tsv"
