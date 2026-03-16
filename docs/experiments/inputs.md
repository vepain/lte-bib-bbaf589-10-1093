---
icon: lucide/file-input
---

# Formatting data in PlasEval format

>[!IMPORTANT]
> Make sure you have installed the `lteu` package.

```sh
.
└── data
    ├── original  # Original data
    │   └── predictions.xlsx
    ├── ground_truths  # PlasEval formatted ground-truths
    │   ├── only_plasmids
    │   └── with_chromosomes
    └── binning  # PlasEval formatted bins
        ├── only_plasmids
        │   └── $tool
        └── with_chromosomes  # Same subtree as only_plasmids/
```

```sh
mkdir data
cd data
```

## Format the ground truth to the PlasEval format

Without the chromosomal bin:

```sh
lteu fmt plaseval gt original/predictions.xlsx ground_truths/only_plasmids
```

With the chromosomal bin:

```sh
lteu fmt plaseval gt original/predictions.xlsx ground_truths/with_chromosomes
```

## Format the bins to the PlasEval format

Without the chromosomal bin:

```sh
tool=hyasp # mob | pbf | gplas2
lteu fmt plaseval bins original/predictions.xlsx $tool binning/only_plasmids/$tool
```

With the chromosomal bin:

```sh
tool=hyasp # mob | pbf | gplas2
lteu fmt plaseval bins original/predictions.xlsx $tool binning/with_chromosomes/$tool --with-chromosomes
```
