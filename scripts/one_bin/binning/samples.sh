#!/usr/bin/env bash

exp_dir=experiments/one_bin/binning

lteu smp one-bin samples/complete_hybrid_asm.tsv ground_truths/only_plasmids $exp_dir/samples.tsv
