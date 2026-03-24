---
icon: lucide/file-spreadsheet
---

# Configurating the working space

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](/install.md).

<!--  -->

>[!TIP] Keeping in memory the scripts directory absolute path (`$SCRIPTS_DIR` variable)
> Here and for all the experiments, you can use the scripts in the `scripts` directory that is at the root of the git repository.
> We recommend you to save in a bash variable the absolute path to that directory:
>
> <!-- markdownlint-disable MD046 -->
> === "Bash"
>
>     ```sh
>     # In the git repository
>     cd scripts
>     SCRIPTS_DIR=$(pwd -P)
>     ```
>
> === "Fish"
>
>     ```fish
>     # In the git repository
>     cd scripts
>     set SCRIPTS_DIR (pwd -P)
>     ```
> <!-- markdownlint-enable MD046 -->

Create the root directory in which all the experiments will be run. Here we create a `data` directory:

```sh title="Where you want"
mkdir data
cd data
```

<!-- markdownlint-disable MD046 -->
??? tip "Running everything in once"

    You may have to set the `$SCRIPTS_DIR` variable, see above.

    ```sh
    $SCRIPTS_DIR/download_original.sh
    $SCRIPTS_DIR/fmt_samples.sh
    $SCRIPTS_DIR/fmt_gt.sh
    $SCRIPTS_DIR/fmt_binning.sh
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
