---
icon: lucide/telescope
---

# Taking into account the contigs lengths and visualizing the chromosomal bin bias

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](/install.md).

<!--  -->

>[!IMPORTANT]
> The following commands are run in the `data` directory.
>
> ```sh
> cd data
> ```

Initializing the experiment:

```sh
exp_dir=experiments/overview
mkdir -p $exp_dir
```

<!-- markdownlint-disable MD046 -->
??? tip "Running everything in once"

    You may have to initialize the `$SCRIPTS_DIR` variable, see [Configurating the working space](/inputs.md).

    ```sh
    $SCRIPTS_DIR/evals.sh
    $SCRIPTS_DIR/merge_evals.sh
    $SCRIPTS_DIR/fig_dist.sh
    $SCRIPTS_DIR/fig_dist_content.sh
    $SCRIPTS_DIR/fig_dist_mode.sh
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
    ├── 📁 binning  # PlasEval formatted bins
    │   ├── 📁 only_plasmids
    │   │   └── 📁 $tool
    │   └── 📁 with_chromosomes  # Same subtree as only_plasmids/
    └── 📁 experiments
        └── overview
            ├── 📁 evals
            │   ├── 📁 only_plasmids
            │   │   ├── $tool.tsv
            │   │   └── merge.tsv
            │   └── 📁 with_chromosomes # Same subtree as only_plasmids/
            └── figs
    ```
<!-- markdownlint-enable MD046 -->

## Evaluating the completeness and the homogeneity

Two measures modes:

* Unweighted completeness and homogeneity
* Weighted completeness and homogeneity (by the contigs lengths)

Two bin contents:

* Only plasmid bins (`📁 only_plasmids`)
* Plasmid and chromosomal bins (`📁 with_chromosomes`)

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/overview/evals.sh"
    --8<-- "scripts/overview/evals.sh"
    ```
<!-- markdownlint-enable MD046 -->

### Merge the evaluations

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/overview/merge_evals.sh"
    --8<-- "scripts/overview/merge_evals.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Generating figures

### The full distributions figure

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/overview/fig_dist.sh"
    --8<-- "scripts/overview/fig_dist.sh"
    ```
<!-- markdownlint-enable MD046 -->

!!! note "Figure"

    [Distribution](figs/distributions.pdf){ target="_blank" } <!--  markdownlint-disable MD046  -->

### Easier-to-read figures

#### Comparing the only plasmids and the with chromosomes cases

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/overview/fig_dist_content.sh"
    --8<-- "scripts/overview/fig_dist_content.sh"
    ```
<!-- markdownlint-enable MD046 -->

??? note "Figures"

    [Unweighted distributions](figs/distributions_content_Unweighted.pdf){ target="_blank" } <!--  markdownlint-disable MD046  -->

    [Weighted distributions](figs/distributions_content_Weighted.pdf){ target="_blank" }

#### Comparing the unweighted and weighted completeness and homogeneity

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/overview/fig_dist_mode.sh"
    --8<-- "scripts/overview/fig_dist_mode.sh"
    ```
<!-- markdownlint-enable MD046 -->

??? note "Figures"

    [Only plasmids distributions](figs/distributions_mode_only_plasmids.pdf){ target="_blank" } <!--  markdownlint-disable MD046  -->

    [With chromosomes distributions](figs/distributions_mode_with_chromosomes.pdf){ target="_blank" }
