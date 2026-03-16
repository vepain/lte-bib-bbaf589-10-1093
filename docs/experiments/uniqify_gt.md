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

<!-- TODO samples only with repeats -->

Manually:

```sh
content=only_plasmids # | with_chromosomes
lteu uniqify gt ground_truths/$content samples/repeats/$content.tsv uniqify/$content/ground_truths
```

Or executing the script `scripts/uniqify/ground_truths/inputs.sh` in `data` directory.

## Evaluating the completeness and the homogeneity

### Without uniqify

```sh
content=only_plasmids # | with_chromosomes
gt_dir=ground_truths/$content
lteu eval $gt_dir $gt_dir samples/repeats/$content.tsv comp_hom/$content/repeats/ground_truths.tsv
```

Or executing the script `scripts/uniqify/ground_truths/eval_repeats.sh` in `data` directory.

### With uniqify

```sh
content=only_plasmids # | with_chromosomes
gt_dir=uniqify/$content/ground_truths
lteu eval $gt_dir $gt_dir samples/repeats/$content.tsv comp_hom/$content/uniqify/ground_truth.tsv
```

Or executing the script `scripts/uniqify/ground_truths/eval_uniqify.sh` in `data` directory.
