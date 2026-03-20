---
icon: lucide/file-spreadsheet
---

# Formatting data in PlasEval format

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](../install.md).

```sh
mkdir data
cd data
```

<!-- markdownlint-disable MD046 -->
??? tip "Running everything in once"

    ```sh
    scripts_dir=scripts/inputs  # use the correct path (absolute path recommended)

    $scripts_dir/download_original.sh
    $scripts_dir/fmt_samples.sh
    $scripts_dir/fmt_gt.sh
    $scripts_dir/fmt_binning.sh
    ```
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
??? info "File tree structure"

    ```sh
    📁 data
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
<!-- markdownlint-enable MD046 -->

The next sections detail the experiment steps.

## Download the original data

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/inputs/download_original.sh"
    --8<-- "scripts/inputs/download_original.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Format the samples to the PlasEval format

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/inputs/fmt_samples.sh"
    --8<-- "scripts/inputs/fmt_samples.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Format the ground truths to the PlasEval format

Ground truths with only plasmid bins, and with chromosomal bin.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/inputs/fmt_gt.sh"
    --8<-- "scripts/inputs/fmt_gt.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Format the bins to the PlasEval format

Binning predictions with only plasmid bins, and with chromosomal bin.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/inputs/fmt_binning.sh"
    --8<-- "scripts/inputs/fmt_binning.sh"
    ```
<!-- markdownlint-enable MD046 -->

<!--  -->

>[!NOTE]
> gplas2 can label a contig `Unbinned_k`, with `k` an integer. In that case, we consider the contig labelled chromosome.
