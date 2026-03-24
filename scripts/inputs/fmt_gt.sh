#!/usr/bin/env bash

# Only plasmid ground truth bins
lteu fmt ground-truths original/predictions.xlsx ground_truths/only_plasmids

# Ground truth plasmid and chromosomal bins
lteu fmt ground-truths original/predictions.xlsx ground_truths/with_chromosomes --with-chromosomes
