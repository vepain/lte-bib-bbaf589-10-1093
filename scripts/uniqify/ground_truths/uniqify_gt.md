---
icon: lucide/copy
---

# Repeat bias

>[!IMPORTANT]
> Make sure you have installed the `lteu` package.

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
    │   └── with_chromosomes  # Same subtree as only_plasmids/
    ├── uniqify  # Predictions and ground-truths after uniqify (complete hybrid assemblies only)
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

Manually:

```sh
content=only_plasmids # | with_chromosomes
lteu ops uniqify gt ground_truths/$content samples/complete_hybrid_asm.tsv uniqify/$content/ground_truths
```

Or executing the script `scripts/uniqify/ground_truths/inputs.sh` in `data` directory.

## Evaluating the completeness and the homogeneity

### Without uniqify

```sh
content=only_plasmids # | with_chromosomes
gt_tsv=ground_truths/$content
lteu eval $gt_tsv $gt_tsv samples/complete_hybrid_asm.tsv comp_hom/$content/repeats/ground_truths.tsv
```

Or executing the script `scripts/uniqify/ground_truths/eval_repeats.sh` in `data` directory.

Merge the evaluations:

```sh
content=only_plasmids # | with_chromosomes
eval_dir=comp_hom/$content/repeats
lteu fmt merge-eval \
    -i $eval_dir/hyasp.tsv -t hyasp \
    -i $eval_dir/mob.tsv -t mob \
    -i $eval_dir/pbf.tsv -t pbf \
    -i $eval_dir/gplas2.tsv -t gplas2 \
    $eval_dir/merge.tsv
```

### With uniqify

```sh
tool=hyasp # mob | pbf | gplas2
content=only_plasmids # | with_chromosomes
lteu eval uniqify/$content/$tool/binning uniqify/$content/$tool/ground_truths samples/complete_hybrid_asm.tsv comp_hom/$content/uniqify/$tool.tsv
```

Or executing the script `scripts/uniqify/tools/eval_uniqify.sh` in `data` directory.

Merge the evaluations:

```sh
content=only_plasmids # | with_chromosomes
eval_dir=comp_hom/$content/uniqify
lteu fmt merge-eval \
    -i $eval_dir/hyasp.tsv -t hyasp \
    -i $eval_dir/mob.tsv -t mob \
    -i $eval_dir/pbf.tsv -t pbf \
    -i $eval_dir/gplas2.tsv -t gplas2 \
    $eval_dir/merge.tsv
```
