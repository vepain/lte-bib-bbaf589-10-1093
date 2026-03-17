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
    │   ├── complete_hybrid_asm.tsv
    │   └── repeats  # samples with repeats in ground truth bins
    │       ├── only_plasmids.tsv
    │       └── with_chromosomes.tsv
    ├── ground_truths  # PlasEval formatted ground-truths
    │   ├── only_plasmids
    │   └── with_chromosomes
    ├── binning  # PlasEval formatted bins
    │   ├── only_plasmids
    │   │   └── $tool
    │   └── with_chromosomes  # Same subtree as only_plasmids/
    ├── uniqify  # Predictions and ground-truths after uniqify (complete hybrid assemblies only and with repeats)
    │   ├── only_plasmids
    │   │   └── ground_truths # Same subtree as in ground_truths/only_plasmids/
    │   └── with_chromosomes # Same subtree as only_plasmids/
    └── comp_hom  # Completeness and homogeneity (complete hybrid assemblies only)
        ├── only_plasmids
        │   ├── repeats
        │   │   └── ground_truth.tsv
        │   └── uniqify
        │       └── ground_truth.tsv
        └── with_chromosomes # Same subtree as only_plasmids/
```

```sh
cd data
```

## Preparing the input data

### Get the list of samples for which there are repeats among the ground-truth bins

```sh
content=only_plasmids # | with_chromosomes
lteu smp repeats samples/complete_hybrid_asm.tsv ground_truths/$content samples/repeats/$content.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/sampling.sh` in the `data` directory.

<!-- to avoid merge of admonitions -->

>[!NOTE]
> The lists from `only_plasmids` and `with_chromosomes` must be the same.
> In fact, authors wrote
>
> !!! quote
>
>     Contigs mapping equally well to a hybrid-assembly chromosome and plasmid contig were excluded from downstream analyses. <!--  markdownlint-disable MD046  -->

### Create the uniqify versions of the samples

`uniqify` command formats the contig names such that there is a null contig names intersection between the ground-truth bins:

```sh
content=only_plasmids # | with_chromosomes
lteu uniqify gt ground_truths/$content samples/repeats/$content.tsv uniqify/$content/ground_truths
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/inputs.sh` in the `data` directory.

## Evaluating the completeness and the homogeneity

### Without uniqify

```sh
content=only_plasmids # | with_chromosomes
gt_dir=ground_truths/$content
lteu eval $gt_dir $gt_dir samples/repeats/$content.tsv comp_hom/$content/repeats/ground_truths.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/eval_repeats.sh` in the `data` directory.

### With uniqify

```sh
content=only_plasmids # | with_chromosomes
gt_dir=uniqify/$content/ground_truths
lteu eval $gt_dir $gt_dir samples/repeats/$content.tsv comp_hom/$content/uniqify/ground_truth.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/eval_uniqify.sh` in the `data` directory.

## Generating figures

```sh
content=only_plasmids # | with_chromosomes
measure="unw_comp" # | unw_hom | w_comp | w_hom

x_evals_tsv=comp_hom/$content/repeats/ground_truths.tsv
x_label="Original"

y_evals_tsv=comp_hom/$content/uniqify/ground_truth.tsv
y_label="Uniqify"

fig_pdf="figs/uniqify/$content/ground_truths/$measure.pdf"

lteu figs vs gt "$measure" "$fig_pdf" \
    --x-axis "$x_evals_tsv" --x-label "$x_label" \
    --y-axis "$y_evals_tsv" --y-label "$y_label"
```

>[!TIP]
> You can execute the script `scripts/uniqify/ground_truths/fig_vs.sh` in the `data` directory.
