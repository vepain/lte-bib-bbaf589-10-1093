#!/bin/bash
# ---------------------------------------------------------------------------- #
# SLURM script for job resubmission on our clusters.
# ---------------------------------------------------------------------------- #
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH --time=3:00:00
#SBATCH --account=def-chauvec
#SBATCH --output=/scratch/vepain/2026_letter_to_editor/fmt/bins/stdout.log
#SBATCH --error=/scratch/vepain/2026_letter_to_editor/fmt/bins/stderr.log
#SBATCH --mail-user=victorepain@disroot.org
#SBATCH --mail-type=ALL

umask 007

home_dir="/project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/"

data_dir="$home_dir/data"

original_predictions="$data_dir/original/predictions.xlsx"
bins_dir="$data_dir/binning/"

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

tools="hyasp mob pbf gplas2"
for tool in $tools; do
    bin_content_dir="$bins_dir/only_plasmids/$tool"
    mkdir -p "$bin_content_dir"
    lteu fmt bins-to-plaseval "$original_predictions" "$tool" "$bin_content_dir"

    bin_content_dir="$bins_dir/with_chromosomes/$tool"
    mkdir -p "$bin_content_dir"
    lteu fmt bins-to-plaseval "$original_predictions" "$tool" "$bin_content_dir" --with-chromosomes
done
