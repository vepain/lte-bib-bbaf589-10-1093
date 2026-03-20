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

The `lteu exp init` command will create the above directory structure.

```sh
lteu exp init data
```

<!--  -->

>[!NOTE]
> gplas2 can label a contig `Unbinned_k`, with `k` an integer. In that case, we consider the contig labelled chromosome.
