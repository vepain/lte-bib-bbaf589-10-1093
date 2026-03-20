#!/usr/bin/env bash

# ------------------------------------------------------------------------------------ #
# Experiment: one bin for tools
# ------------------------------------------------------------------------------------ #
rm_samples_mode="fails" # | nothing
#
# Figures aesthetics
#
context=paper
focus_mode="--full" # | --focus
# ------------------------------------------------------------------------------------ #

echo "EXPERIMENT: ONE BIN FOR TOOLS"

declare -r exp_dir="experiments/one_bin/binning"

declare -r contents="only_plasmids with_chromosomes"

declare -r tools="hyasp mob pbf gplas2"

declare -r exp_samples="$exp_dir/samples.tsv"

init() {
    echo
    echo "Init experiment"
    echo

    mkdir -p "$exp_dir" 2>/dev/null
}

smp() {
    echo
    echo "Sampling"
    echo

    uv run lteu smp one-bin samples/complete_hybrid_asm.tsv ground_truths/only_plasmids "$exp_samples"
}

evals() {
    echo
    echo "Evaluating"
    echo
    for content in $contents; do
        for tool in $tools; do
            uv run lteu eval run "binning/$content/$tool" "ground_truths/$content" "$exp_samples" "$exp_dir/evals/$content/$tool.tsv"
        done
    done
}

merge-evals() {
    echo
    echo "Merging evals"
    echo

    for content in $contents; do

        local sopt_tools=()
        for tool in $tools; do
            sopt_tools+=(--tool-code "$tool")
            sopt_tools+=(--eval-tsv "$exp_dir/evals/$content/$tool.tsv")
        done

        uv run lteu eval merge \
            "${sopt_tools[@]}" \
            "$exp_dir/evals/$content/merge.tsv"
    done
}

fig-dist() {
    echo
    echo "Generating full distribution figure"
    echo

    if [[ -z "$1" ]]; then
        echo "[ERROR] No tools provided"
        exit 1
    fi
    local user_tools="$1"

    local only_plm_tools_evals_tsv="$exp_dir/evals/only_plasmids/merge.tsv"
    local with_chm_tools_evals_tsv="$exp_dir/evals/with_chromosomes/merge.tsv"

    local fig_pdf="$exp_dir/figs/distributions.pdf"

    local sopt_tools=()
    for tool in $user_tools; do
        sopt_tools+=(--tool "$tool")
    done

    uv run lteu figs dist tools \
        "$only_plm_tools_evals_tsv" "$with_chm_tools_evals_tsv" "$fig_pdf" \
        "${sopt_tools[@]}" \
        --remove-samples "$rm_samples_mode" \
        --context "$context" "$focus_mode"
}

case "$1" in
"") ;;
init)
    init
    ;;
smp)
    smp
    ;;
evals)
    evals
    ;;
merge-evals)
    merge-evals
    ;;
fig-dist)
    fig-dist "$2"
    ;;
*)
    echo "Unknown command: $1"
    exit 1
    ;;
esac
