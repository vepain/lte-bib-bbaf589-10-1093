# Binning tools versus the ground truths

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

<!-- DOCU Commands -->

## Generating figures

### Versus figures

<!--  markdownlint-disable MD046  -->
??? note "Figures"

    [Unweighted completeness](figs/unw_comp.pdf){ target="_blank" }

    [Unweighted homogeneity](figs/unw_hom.pdf){ target="_blank" }

    [Weighted completeness](figs/w_comp.pdf){ target="_blank" }

    [Weighted homogeneity](figs/w_hom.pdf){ target="_blank" }
<!--  markdownlint-enable MD046  -->

### Distributions figures

<!--  markdownlint-disable MD046  -->
??? note "Figures"

    [All the tools](figs/distribution.pdf){ target="_blank" }

    [Without PlasBin-flow](figs/distribution_no_pbf.pdf){ target="_blank" }
<!--  markdownlint-enable MD046  -->