---
icon: lucide/copy
status: deprecated
---

# Repeat bias for each tool

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](/install.md).

<!--  -->

!!! danger

    The following section is old such that some informations may be out of date.  <!-- markdownlint-disable MD046  -->

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
    │   │   └── $tool
    │   │       ├── binning # one file per sample
    │   │       ├── ground_truths # idem
    │   │       └── nb_matches.tsv
    │   └── with_chromosomes # Same subtree as only_plasmids/
    └── comp_hom  # Completeness and homogeneity (complete hybrid assemblies only)
        ├── only_plasmids
        │   ├── repeats
        │   │   └── $tool.tsv
        │   └── uniqify # Same subtree as repeats/
        └── with_chromosomes # Same subtree as only_plasmids/
```

```sh
cd data
```

## Preparing the input data

Manually:

```sh
tool=hyasp # mob | pbf | gplas2
content=only_plasmids # | with_chromosomes
lteu uniqify tool binning/$content/$tool ground_truths/$content samples/complete_hybrid_asm.tsv uniqify/$content/$tool
```

Or executing the script `scripts/uniqify/tools/inputs.sh` in `data` directory.

## Evaluating the completeness and the homogeneity

### Without uniqify

```sh
tool=hyasp # mob | pbf | gplas2
content=only_plasmids # | with_chromosomes
lteu eval run binning/$content/$tool ground_truths/$content samples/complete_hybrid_asm.tsv comp_hom/$content/repeats/$tool.tsv
```

Or executing the script `scripts/uniqify/tools/eval_repeats.sh` in `data` directory.

Merge the evaluations:

```sh
content=only_plasmids # | with_chromosomes
eval_dir=comp_hom/$content/repeats
lteu eval merge \
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
lteu eval run uniqify/$content/$tool/binning uniqify/$content/$tool/ground_truths samples/complete_hybrid_asm.tsv comp_hom/$content/uniqify/$tool.tsv
```

Or executing the script `scripts/uniqify/tools/eval_uniqify.sh` in `data` directory.

Merge the evaluations:

```sh
content=only_plasmids # | with_chromosomes
eval_dir=comp_hom/$content/uniqify
lteu eval merge \
    -i $eval_dir/hyasp.tsv -t hyasp \
    -i $eval_dir/mob.tsv -t mob \
    -i $eval_dir/pbf.tsv -t pbf \
    -i $eval_dir/gplas2.tsv -t gplas2 \
    $eval_dir/merge.tsv
```
