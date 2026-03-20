---
icon: lucide/file-spreadsheet
---

# Formatting data in PlasEval format

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](../install.md).

```sh
.
└── 📁 data
    ├── 📁 original  # Original data
    │   └── predictions.xlsx
    ├── 📁 samples
    │   └── complete_hybrid_asm.tsv
    ├── 📁 ground_truths  # PlasEval formatted ground-truths
    │   ├── 📁 only_plasmids
    │   └── 📁 with_chromosomes
    └── 📁 binning  # PlasEval formatted bins
        ├── 📁 only_plasmids
        │   └── 📁 $tool
        └── 📁 with_chromosomes  # Same subtree as only_plasmids/
```

```sh
mkdir data
cd data
```

<!-- DOCU write the full commands in once -->

## Download the original data

```sh
wget https://github.com/broadinstitute/plasmid-detection-benchmark/raw/refs/heads/main/data/predictions.xlsx -O original/predictions.xlsx
```

## Format the samples to the PlasEval format

```sh
lteu fmt samples original/predictions.xlsx samples/complete_hybrid_asm.tsv
```

## Format the ground truth to the PlasEval format

Without the chromosomal bin:

```sh
lteu fmt ground-truths original/predictions.xlsx ground_truths/only_plasmids
```

With the chromosomal bin:

```sh
lteu fmt ground-truths original/predictions.xlsx ground_truths/with_chromosomes --with-chromosomes
```

## Format the bins to the PlasEval format

Without the chromosomal bin:

```sh
tool=hyasp # mob | pbf | gplas2
lteu fmt bins original/predictions.xlsx $tool binning/only_plasmids/$tool
```

>[!TIP]
> You can execute the script `scripts/inputs/only_plasmids.sh` in the `data` directory.

With the chromosomal bin:

```sh
tool=hyasp # mob | pbf | gplas2
lteu fmt bins original/predictions.xlsx $tool binning/with_chromosomes/$tool --with-chromosomes
```

>[!TIP]
> You can execute the script `scripts/inputs/with_chromosomes.sh` in the `data` directory.

<!--  -->

>[!NOTE]
> gplas2 can label a contig `Unbinned_k`, with `k` an integer. In that case, we consider the contig labelled chromosome.
