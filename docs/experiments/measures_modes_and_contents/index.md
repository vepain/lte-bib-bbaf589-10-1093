---
icon: lucide/ungroup
---

# Measures modes and bins content

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
            │   └──  evals
            │       ├── $tool.tsv
            │       └── merge.tsv
            ├── with_chromosomes # Same subtree as experiments/chromosomes/only_plasmids/
            └── figs
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

### The full distributions figure

To generate a complete figure of the distributions.

```sh
only_plm_tools_evals_tsv=$exp_dir/only_plasmids/evals/merge.tsv
with_chm_tools_evals_tsv=$exp_dir/with_chromosomes/evals/merge.tsv

fig_pdf="$exp_dir/figs/distribution.pdf"

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

??? note "Figure"

    [Distribution](figs/distribution.pdf){ target="_blank" } <!--  markdownlint-disable MD046  -->

### Easier-to-read figures

#### Comparing the only plasmids and the with chromosomes cases

```sh
mode=Unweighted # | Weighted

only_plm_tools_evals_tsv=$exp_dir/only_plasmids/evals/merge.tsv
with_chm_tools_evals_tsv=$exp_dir/with_chromosomes/evals/merge.tsv

fig_pdf="$exp_dir/figs/distribution_content_$mode.pdf"

lteu figs dist tools-content \
    $only_plm_tools_evals_tsv $with_chm_tools_evals_tsv $mode $fig_pdf \
    --tool hyasp \
    --tool mob \
    --tool pbf \
    --tool gplas2 \
    --remove-samples fails
```

>[!TIP]
> You can execute the script `scripts/chromosomes/fig_dist_content.sh` in the `data` directory.

??? note "Figures"

    [Unweighted distributions](figs/distribution_content_Unweighted.pdf){ target="_blank" } <!--  markdownlint-disable MD046  -->

    [Weighted distributions](figs/distribution_content_Weighted.pdf){ target="_blank" }

#### Comparing the unweighted and weighted completeness and homogeneity

```sh
content=only_plasmids # | with_chromosomes

only_plm_tools_evals_tsv=$exp_dir/only_plasmids/evals/merge.tsv
with_chm_tools_evals_tsv=$exp_dir/with_chromosomes/evals/merge.tsv

fig_pdf="$exp_dir/figs/distribution_mode_$content.pdf"

lteu figs dist tools-mode \
    $only_plm_tools_evals_tsv $with_chm_tools_evals_tsv $content $fig_pdf \
    --tool hyasp \
    --tool mob \
    --tool pbf \
    --tool gplas2 \
    --remove-samples fails
```

>[!TIP]
> You can execute the script `scripts/chromosomes/fig_dist_mode.sh` in the `data` directory.

??? note "Figures"

    [Only plasmids distributions](figs/distribution_mode_only_plasmids.pdf){ target="_blank" } <!--  markdownlint-disable MD046  -->

    [With chromosomes distributions](figs/distribution_mode_with_chromosomes.pdf){ target="_blank" }
