---
icon: lucide/ungroup
---

# Chromosomal bin bias

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](../install.md).

```sh
.
└── data
    ├── samples
    │   └── complete_hybrid_asm.tsv
    ├── ground_truths  # PlasEval formatted ground-truths
    │   ├── only_plasmids
    │   └── with_chromosomes
    ├── binning  # PlasEval formatted bins
    │   ├── only_plasmids
    │   │   └── $tool
    │   └── with_chromosomes  # Same subtree as binning/only_plasmids/
    └── experiments
        └── chromosomes
            ├── only_plasmids
            │   ├── evals
            │   │   ├── $tool.tsv
            │   │   └── merge.tsv
            │   └── figs # Contains figures in PDF format
            ├── with_chromosomes # Same subtree as experiments/chromosomes/only_plasmids/
            └── figs
                └── distributions.pdf
```

>[!IMPORTANT]
> The following commands are run in the `data` directory.
>
> ```sh
> cd data
> ```

## Initializing the experiment space

```sh
exp_dir=experiments/chromosomes
mkdir -p $exp_dir
```

## Evaluating the completeness and the homogeneity

```sh
content=only_plasmids # | with_chromosomes
tool=hyasp # mob | pbf | gplas2

lteu eval run binning/$content/$tool ground_truths/$content samples/complete_hybrid_asm.tsv $exp_dir/$content/evals/$tool.tsv
```

>[!TIP]
> You can execute the script `scripts/chromosomes/evals.sh` in the `data` directory.

### Merge the evaluations

```sh
content=only_plasmids # | with_chromosomes

lteu eval merge \
    -t hyasp -i $exp_dir/$content/evals/hyasp.tsv \
    -t mob -i $exp_dir/$content/evals/mob.tsv \
    -t pbf -i $exp_dir/$content/evals/pbf.tsv \
    -t gplas2 -i $exp_dir/$content/evals/gplas2.tsv \
    $exp_dir/$content/evals/merge.tsv
```

>[!TIP]
> You can execute the script `scripts/chromosomes/merge_evals.sh` in the `data` directory.

## Generating figures

### The distributions figure

```sh
only_plm_tools_evals_tsv=$exp_dir/only_plasmids/evals/merge.tsv
with_chm_tools_evals_tsv=$exp_dir/with_chromosomes/evals/merge.tsv

fig_pdf="$exp_dir/figs/distributions.pdf"

lteu figs dist tools \
    $only_plm_tools_evals_tsv $with_chm_tools_evals_tsv $fig_pdf \
    --tool hyasp \
    --tool mob \
    --tool pbf \
    --tool gplas2 \
    --remove-samples fails
```

>[!TIP]
> You can execute the script `scripts/chromosomes/fig_dist.sh` in the `data` directory.
