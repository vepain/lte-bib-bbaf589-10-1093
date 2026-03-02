#!/bin/bash
# ---------------------------------------------------------------------------- #
# SLURM script for job resubmission on our clusters.
# ---------------------------------------------------------------------------- #
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH --time=3:00:00
#SBATCH --account=def-chauvec
#SBATCH --output=/scratch/vepain/2026_letter_to_editor/fmt/gt/stdout.log
#SBATCH --error=/scratch/vepain/2026_letter_to_editor/fmt/gt/stderr.log
#SBATCH --mail-user=victorepain@disroot.org
#SBATCH --mail-type=ALL

umask 007

home_dir="/project/6001426/wg-anoph/benchmarking/2026_letter_to_editor/"

data_dir="$home_dir/data"

original_predictions="$data_dir/original/predictions.xlsx"
gt_dir="$data_dir/ground_truth/"

tools_dir="$home_dir/tools"
lteu_dir="$tools_dir/lte-bib-bbaf589-10-1093"

# ------------------------------------------------------------------------------------ #
# Install environment
# ------------------------------------------------------------------------------------ #
module load python/3.13
virtualenv --no-download "$SLURM_TMPDIR/env"
# shellcheck disable=SC1091
source "$SLURM_TMPDIR/env/bin/activate"
pip install uv-build
pip install "$lteu_dir"
# ------------------------------------------------------------------------------------ #

gt_content_dir="$gt_dir/only_plasmids"
mkdir -p "$gt_content_dir"
lteu fmt gt-to-plaseval "$original_predictions" "$gt_content_dir"

gt_content_dir="$gt_dir/with_chromosome"
mkdir -p "$gt_content_dir"
lteu fmt gt-to-plaseval "$original_predictions" "$gt_content_dir" --with-chromosome
