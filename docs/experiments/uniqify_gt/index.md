---
icon: lucide/copy
---

# Repeat bias

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
                └── with_chromosomes # Same subtree as experiments/uniqify/only_plasmids/
```

>[!IMPORTANT]
> The following commands are run in the `data` directory.
>
> ```sh
> cd data
> ```

## Initializing the experiment space

```sh
exp_dir=experiments/uniqify/ground_truths
mkdir -p $exp_dir
```

## Preparing the input data

### Get the list of samples for which there are repeats among the ground-truth bins

```sh
content=only_plasmids # | with_chromosomes
lteu smp repeats samples/complete_hybrid_asm.tsv ground_truths/$content $exp_dir/$content/samples.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/sampling.sh` in the `data` directory.

<!-- to avoid merge of admonitions -->

>[!NOTE]
> The sample lists from `only_plasmids` and `with_chromosomes` must be the same.
> In fact, authors wrote
>
> !!! quote
>
>     Contigs mapping equally well to a hybrid-assembly chromosome and plasmid contig were excluded from downstream analyses. <!--  markdownlint-disable MD046  -->

### Create the uniqify versions of the ground truth bins

`uniqify` command formats the contig names such that there is a null contig names intersection between the ground-truth bins:

```sh
content=only_plasmids # | with_chromosomes
lteu uniqify gt ground_truths/$content $exp_dir/$content/samples.tsv $exp_dir/$content/ground_truths
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/inputs.sh` in the `data` directory.

## Evaluating the completeness and the homogeneity

For each of the ground truths (original and uniqified), we provide the completeness and the homogeneity measures by evaluating the ground truth bins against themselves.

### Without uniqify

```sh
content=only_plasmids # | with_chromosomes
gt_dir=ground_truths/$content
lteu eval $gt_dir $gt_dir $exp_dir/$content/samples.tsv $exp_dir/$content/evals/repeats.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/eval_repeats.sh` in the `data` directory.

### With uniqify

```sh
content=only_plasmids # | with_chromosomes
gt_dir=$exp_dir/$content/ground_truths
lteu eval $gt_dir $gt_dir $exp_dir/$content/samples.tsv $exp_dir/$content/evals/uniqify.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/eval_uniqify.sh` in the `data` directory.

## Generating figures

### The versus figure (original ground truths vs uniqified ground truths)

```sh
content=only_plasmids # | with_chromosomes
measure="unw_comp" # | unw_hom | w_comp | w_hom

x_evals_tsv=$exp_dir/$content/evals/repeats.tsv
x_label="Original"

y_evals_tsv=$exp_dir/$content/evals/uniqify.tsv
y_label="Uniqify"

fig_pdf="$exp_dir/$content/figs/$measure.pdf"

lteu figs vs gt "$measure" "$fig_pdf" \
    --x-axis "$x_evals_tsv" --x-label "$x_label" \
    --y-axis "$y_evals_tsv" --y-label "$y_label"
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/fig_vs.sh` in the `data` directory.

??? note "Figures for only plasmids"

    [Unweighted completeness](figs/only_plasmids/unw_comp.pdf){ target="_blank" }

    [Unweighted homogeneity](figs/only_plasmids/unw_hom.pdf){ target="_blank" }

    [Weighted completeness](figs/only_plasmids/w_comp.pdf){ target="_blank" }

    [Weighted homogeneity](figs/only_plasmids/w_hom.pdf){ target="_blank" }

??? note "Figures for with chromosomes"

    [Unweighted completeness](figs/with_chromosomes/unw_comp.pdf){ target="_blank" }

    [Unweighted homogeneity](figs/with_chromosomes/unw_hom.pdf){ target="_blank" }

    [Weighted completeness](figs/with_chromosomes/w_comp.pdf){ target="_blank" }

    [Weighted homogeneity](figs/with_chromosomes/w_hom.pdf){ target="_blank" }

### The distribution of the measures for the original ground truths

As for the uniqified ground truths the measures all equal to 1 (theoretically expected, one can verify that on the previous versus figures)

```sh
only_plm_eval_tsv=$exp_dir/only_plasmids/evals/repeats.tsv
with_chm_eval_tsv=$exp_dir/with_chromosomes/evals/repeats.tsv

fig_pdf="$exp_dir/figs/distributions.pdf"

lteu figs uniqify gt dist "$only_plm_eval_tsv" "$with_chm_eval_tsv" "$fig_pdf"
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/fig_dist.sh` in the `data` directory.

??? note "Figure"

    [Distribution](figs/distribution.pdf){ target="_blank" }
