#!/bin/bash
# ---------------------------------------------------------------------------- #
# SLURM script for job resubmission on our clusters.
# ---------------------------------------------------------------------------- #
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=12:00:00
#SBATCH --account=def-chauvec
#SBATCH --array=2-206
#SBATCH --output=/scratch/vepain/2026_letter_to_editor/plaseval/comp/%A/%a.out
#SBATCH --error=/scratch/vepain/2026_letter_to_editor/plaseval/comp/%A/%a.err
#SBATCH --mail-user=victorepain@disroot.org
#SBATCH --mail-type=ALL
# ---------------------------------------------------------------------------- #
# User Variables
# ---------------------------------------------------------------------------- #
declare -r content="only_plasmids" # In only_plasmids, with_chromosome
declare -r method_code="hyasp"     # In hyasp, mob, pbf, gplas2
declare -r alpha=0.5               # between 0 and 1
# ---------------------------------------------------------------------------- #

umask 007

# Get sample ID
#
# Arguments:
# 1. Samples file
#
# Usage:
#   > spe_smp_id=$(get_smp_id_from_file "$samples_file")
function get_smp_id_from_file {
    local smp_file=$1

    sed -n "${SLURM_ARRAY_TASK_ID}p" "$smp_file" | cut -f1
}
# ---------------------------------------------------------------------------- #
# Set directory paths
# ---------------------------------------------------------------------------- #
wg_anoph_bench_dir="/project/def-chauvec/wg-anoph/benchmarking"
letter_to_editor_dir="$wg_anoph_bench_dir/2026_letter_to_editor"

data_dir="$letter_to_editor_dir/data"

gt_dir="$data_dir/ground_truth/$content"
bins_dir="$data_dir/binning/$content/$method_code"

alpha_dir="alpha_${alpha//./}"
eval_dir="$data_dir/plaseval/$content/comp/$alpha_dir/$method_code"

samples_tsv="$data_dir/samples/complete_hybrid_asm.tsv"

tools_dir="$letter_to_editor_dir/tools"
plaseval_dir="$tools_dir/PlasEval"
# ---------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------ #
# Install environment
# ------------------------------------------------------------------------------------ #
module load python/3.13
module load scipy-stack
virtualenv --no-download "$SLURM_TMPDIR/env"
# shellcheck disable=SC1091
source "$SLURM_TMPDIR/env/bin/activate"
pip install --no-index --upgrade pip
pip install --no-index -r "$plaseval_dir/requirements.txt"
# ------------------------------------------------------------------------------------ #

smp_uid=$(get_smp_id_from_file "$samples_tsv")

echo "$SLURM_ARRAY_TASK_ID $smp_uid $method_code"

# Exit 0 if there is no $file and echo message
if [[ ! -f "$bins_dir/$smp_uid.tsv" ]]; then
    echo "$bins_dir/$smp_uid.tsv does not exist"
    exit 0
fi

#
# Running PlasEval for the method
#
cd "$plaseval_dir/src" || exit 1

python plaseval.py \
    comp \
    --l "$bins_dir/$smp_uid.tsv" \
    --r "$gt_dir/$smp_uid.tsv" \
    --p $alpha \
    --out_file "$eval_dir/$smp_uid.out" \
    --log_file "$eval_dir/$smp_uid.log"

deactivate
