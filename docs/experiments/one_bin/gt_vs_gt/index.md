# Ground truths versus themselves

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
exp_dir=experiments/one_bin/gt_vs_gt

mkdir -p $exp_dir
```

<!-- markdownlint-disable MD046 -->
??? tip "Running everything in once"

    You may have to initialize the `$SCRIPTS_DIR` variable, see [Configurating the working space](/inputs.md).

    ```sh
    $SCRIPTS_DIR/samples.sh
    $SCRIPTS_DIR/evals.sh
    $SCRIPTS_DIR/fig_vs.sh
    $SCRIPTS_DIR/fig_dist.sh
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
    └── 📁 experiments
        └── 📁 one_bin
            └── 📁 gt_vs_gt
                ├── samples.tsv
                ├── 📁 evals
                │   ├── only_plasmids.tsv
                │   └── with_chromosomes.tsv
                └── 📁 figs # Contains figures in PDF format
    ```
<!-- markdownlint-enable MD046 -->

The next sections detail the experiment steps.

## Get the list of samples such that the ground truth has only one plasmid bin

It creates the files `gt_vs_gt/samples.tsv`.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/gt_vs_gt/samples.sh"
    --8<-- "scripts/one_bin/gt_vs_gt/samples.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Evaluating the completeness and the homogeneity

It creates the files `gt_vs_gt/evals/only_plasmids.tsv` and `gt_vs_gt/evals/with_chromosomes.tsv`.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/gt_vs_gt/evals.sh"
    --8<-- "scripts/one_bin/gt_vs_gt/evals.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Generating figures

### Versus figures

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/gt_vs_gt/fig_vs.sh"
    --8<-- "scripts/one_bin/gt_vs_gt/fig_vs.sh"
    ```
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
??? note "Figures"

    [Unweighted completeness](figs/unw_comp.pdf){ target="_blank" }

    [Unweighted homogeneity](figs/unw_hom.pdf){ target="_blank" }

    [Weighted completeness](figs/w_comp.pdf){ target="_blank" }

    [Weighted homogeneity](figs/w_hom.pdf){ target="_blank" }
<!-- markdownlint-enable MD046 -->

### Distributions figure

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/one_bin/gt_vs_gt/fig_dist.sh"
    --8<-- "scripts/one_bin/gt_vs_gt/fig_dist.sh"
    ```
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
!!! note "Figure"

    [Distribution](figs/distributions.pdf){ target="_blank" }
<!-- markdownlint-enable MD046 -->
