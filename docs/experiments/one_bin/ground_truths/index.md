# Ground truths versus themselves

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](../install.md).

<!-- DOCU Fix experiment tree -->

```sh
.
└── data
    ├── samples
    │   └── complete_hybrid_asm.tsv
    ├── ground_truths  # PlasEval formatted ground-truths
    │   ├── only_plasmids
    │   └── with_chromosomes
    └── experiments
        └── uniqify
            └── ground_truths
                ├── only_plasmids
                │   ├── samples.tsv
                │   ├── ground_truths
                │   ├── evals
                │   │   ├── repeats.tsv
                │   │   └── uniqify.tsv
                │   └── figs # Contains figures in PDF format
                ├── with_chromosomes # Same subtree as experiments/uniqify/only_plasmids/
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
exp_dir=experiments/one_bin
mkdir -p $exp_dir
```

## Get the list of samples such that the ground truth has only one plasmid bin

```sh
lteu smp one-bin samples/complete_hybrid_asm.tsv ground_truths/only_plasmids $exp_dir/samples.tsv
```

## Evaluating the completeness and the homogeneity

```sh
content=only_plasmids # | with_chromosomes
gt_dir=ground_truths/$content
lteu eval run $gt_dir $gt_dir $exp_dir/samples.tsv $exp_dir/evals/$content.tsv
```

## Generating figures

### Versus figures

>[!TIP]
> You can execute the script `scripts/one_bin/fig_vs.sh` in the `data` directory.

??? note "Figures"

    [Unweighted completeness](figs/unw_comp.pdf){ target="_blank" }  <!--  markdownlint-disable MD046  -->

    [Unweighted homogeneity](figs/unw_hom.pdf){ target="_blank" }

    [Weighted completeness](figs/w_comp.pdf){ target="_blank" }

    [Weighted homogeneity](figs/w_hom.pdf){ target="_blank" }

### Distributions figure

>[!TIP]
> You can execute the script `scripts/one_bin/fig_dist.sh` in the `data` directory.

??? note "Figure"

    [Distribution](figs/distribution.pdf){ target="_blank" }
