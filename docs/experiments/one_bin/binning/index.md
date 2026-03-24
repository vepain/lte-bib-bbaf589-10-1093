# Binning tools versus the ground truths

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](../../../install.md).

<!--  -->

>[!IMPORTANT]
> The following commands are run in the `data` directory.
>
> ```sh
> cd data
> ```

Initializing the experiment:

```sh
exp_dir=experiments/one_bin/binning

mkdir -p $exp_dir
```

<!-- markdownlint-disable MD046 -->
??? tip "Running everything in once"

    You may have to initialize the `$SCRIPTS_DIR` variable, see [Configurating the working space](../../../inputs.md).

    ```sh
    $SCRIPTS_DIR/samples.sh
    $SCRIPTS_DIR/evals.sh
    $SCRIPTS_DIR/merge_evals.sh
    $SCRIPTS_DIR/fig_dist.sh
    $SCRIPTS_DIR/fig_dist_no_pbf.sh
    ```
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
??? info "File tree structure"

    ```sh
    📁 data
    ├── 📁 samples
    │   └── complete_hybrid_asm.tsv
    ├── 📁 ground_truths  # PlasEval formatted ground-truths
    │   ├── 📁 only_plasmids
    │   └── 📁 with_chromosomes
    ├── 📁 binning  # PlasEval formatted binning predictions
    │   ├── 📁 only_plasmids
    │   │   └── 📁 $tool
    │   └── 📁 with_chromosomes  # Same subtree as only_plasmids/
    └── 📁 experiments
        └── 📁 one_bin
            └── 📁 binning
                ├── samples.tsv
                ├── 📁 evals
                │   ├── 📁 only_plasmids
                │   │   └── $tool.tsv
                │   └── 📁 with_chromosomes # Same subtree as only_plasmids/
                └── 📁 figs # Contains figures in PDF format
    ```
<!-- markdownlint-enable MD046 -->

<!-- DOCU Commands -->

The next sections detail the experiment steps.

## Get the list of samples such that the ground truth has only one plasmid bin

It creates the files `binning/samples.tsv`.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/binning/samples.sh"
    --8<-- "scripts/one_bin/binning/samples.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Evaluating the completeness and the homogeneity

For each bin content (only plasmid bins and with chromosomal bin), it creates the files `binning/evals/only_plasmids/$tool.tsv` and `binning/evals/with_chromosomes/$tool.tsv`, where `$tool` is the code of the binning tool (`hyasp`, `mob`, `pbf` or `gplas2`).

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/binning/evals.sh"
    --8<-- "scripts/one_bin/binning/evals.sh"
    ```
<!-- markdownlint-enable MD046 -->

### Merge the evaluations

To create the files `binning/evals/only_plasmids/merge.tsv` and `binning/evals/with_chromosomes/merge.tsv`

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/binning/merge_evals.sh"
    --8<-- "scripts/one_bin/binning/merge_evals.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Generating distributions figures

### With all tools

To create the figure `figs/distributions.pdf`.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/binning/fig_dist.sh"
    --8<-- "scripts/one_bin/binning/fig_dist.sh"
    ```
<!-- markdownlint-enable MD046 -->

<!--  markdownlint-disable MD046  -->
!!! note "Figure"

    [All the tools](figs/distributions.pdf){ target="_blank" }
<!--  markdownlint-enable MD046  -->

### Without PlasBin-flow

Because PlasBin-flow do not return enought results for the subset of samples, we create the figure `figs/distributions_no_pbf.pdf`

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/binning/fig_dist_no_pbf.sh"
    --8<-- "scripts/one_bin/binning/fig_dist_no_pbf.sh"
    ```
<!-- markdownlint-enable MD046 -->

<!--  markdownlint-disable MD046  -->
!!! note "Figure"

    [Without PlasBin-flow](figs/distributions_no_pbf.pdf){ target="_blank" }
<!--  markdownlint-enable MD046  -->