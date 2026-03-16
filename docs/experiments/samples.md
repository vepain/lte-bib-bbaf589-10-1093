---
icon: lucide/filter
---

# Sub-sampling

As in the paper, we consider the samples for which the hybrid assemblies are complete.

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation].

```sh
.
└── data
    ├── original  # Original data
    │   └── predictions.xlsx
    └── samples
        └── complete_hybrid_asm.tsv
```

[Installation]: ../install.md

```sh
cd data
```

```sh
lteu fmt smp complete-hybrid-asm original/predictions.xlsx samples/complete_hybrid_asm.tsv
```
