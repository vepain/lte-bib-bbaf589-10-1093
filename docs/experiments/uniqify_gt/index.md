---
icon: lucide/copy
---

# Analyzing the repeat bias

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](../../install.md).

<!--  -->

>[!IMPORTANT]
> The following commands are run in the `data` directory.
>
> ```sh
> cd data
> ```

Initializing the experiment:

```sh
exp_dir=experiments/uniqify/gt_vs_gt

mkdir -p $exp_dir
```

<!-- markdownlint-disable MD046 -->
??? tip "Running everything in once"

    You may have to initialize the `$SCRIPTS_DIR` variable, see [Configurating the working space](../../inputs.md).

    ```sh
    $SCRIPTS_DIR/samples.sh
    $SCRIPTS_DIR/uniqify.sh
    $SCRIPTS_DIR/eval_original.sh
    $SCRIPTS_DIR/eval_uniqify.sh
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
        └── 📁 uniqify
            └── 📁 gt_vs_gt
                ├── samples.tsv  # For only plasmids and with chromosomes versions, as there are no contigs in common between the plasmid bins and the chromosomal bin
                ├── 📁 ground_truths
                │   ├── 📁 only_plasmids # One file per sample
                │   └── 📁 with_chromosomes # idem
                ├── 📁 evals
                │   ├── 📁 only_plasmids
                │   │   ├── original.tsv
                │   │   └── uniqify.tsv
                │   └── 📁 with_chromosomes
                └── 📁 figs # Contains figures in PDF format
                    ├── distributions.pdf
                    ├── 📁 only_plasmids
                    └── 📁 with_chromosomes
    ```
<!-- markdownlint-enable MD046 -->

The next sections detail the experiment steps.

## Preparing the input data

### Get the list of samples for which there are repeats among the ground-truth bins

Create the sample lists `gt_vs_gt/samples.tsv`.

>[!NOTE]
> To create the subsample list, we only consider the ground truth plasmid bins (in `📁 data/ground_truths/only_plasmids`).
> In fact, the subsampling is the same if we consider the ground truth plasmid and chromosomal bins (in `📁 data/ground_truths/with_chromosomes`)
>
> As the authors wrote:
> <!--  markdownlint-disable MD046  -->
> !!! quote
>
>     Contigs mapping equally well to a hybrid-assembly chromosome and plasmid contig were excluded from downstream analyses.
<!--  markdownlint-enable MD046  -->

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/uniqify/gt_vs_gt/samples.sh"
    --8<-- "scripts/uniqify/gt_vs_gt/samples.sh"
    ```
<!-- markdownlint-enable MD046 -->

### Create the uniqify versions of the ground truth bins

For each bin content (only plasmid bins and with chromosomal bin), we create the uniqify versions of the ground truth bins in `📁 gt_vs_gt/ground_truths/only_plasmids` and `📁 gt_vs_gt/ground_truths/with_chromosomes`.

The uniqify versions of the ground truth bins consists in renaming the contigs names such that there is a null contig names intersection between the ground truth bins.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/uniqify/gt_vs_gt/uniqify.sh"
    --8<-- "scripts/uniqify/gt_vs_gt/uniqify.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Evaluating the completeness and the homogeneity

For each of the ground truths (original and uniqified), we provide the completeness and the homogeneity measures by evaluating the ground truth bins against themselves.

### Original ground truths versus themselves

It creates the files `gt_vs_gt/evals/only_plasmids/original.tsv` and `gt_vs_gt/evals/with_chromosomes/original.tsv`.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/uniqify/gt_vs_gt/eval_original.sh"
    --8<-- "scripts/uniqify/gt_vs_gt/eval_original.sh"
    ```
<!-- markdownlint-enable MD046 -->

### Uniqify ground truths versus themselves

It creates the files `gt_vs_gt/evals/only_plasmids/uniqify.tsv` and `gt_vs_gt/evals/with_chromosomess/uniqify.tsv`.

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/uniqify/gt_vs_gt/eval_uniqify.sh"
    --8<-- "scripts/uniqify/gt_vs_gt/eval_uniqify.sh"
    ```
<!-- markdownlint-enable MD046 -->

## Generating figures

### The versus figure (original ground truths vs uniqified ground truths)

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/uniqify/gt_vs_gt/fig_vs.sh"
    --8<-- "scripts/uniqify/gt_vs_gt/fig_vs.sh"
    ```
<!-- markdownlint-enable MD046 -->

<!--  markdownlint-disable MD046  -->
??? note "Figures for only plasmids"

    [Unweighted completeness](figs/only_plasmids/unw_comp.pdf){ target="_blank" }

    [Unweighted homogeneity](figs/only_plasmids/unw_hom.pdf){ target="_blank" }

    [Weighted completeness](figs/only_plasmids/w_comp.pdf){ target="_blank" }

    [Weighted homogeneity](figs/only_plasmids/w_hom.pdf){ target="_blank" }

??? note "Figures for with chromosomes"

    [Unweighted completeness](figs/with_chromosomes/unw_comp.pdf){ target="_blank" }

    [Unweighted homogeneity](figs/with_chromosomes/unw_hom.pdf){ target="_blank" }

    [Weighted completeness](figs/with_chromosomes/w_comp.pdf){ target="_blank" }

    [Weighted homogeneity](figs/with_chromosomes/w_hom.pdf){ target="_blank" }
<!--  markdownlint-enable MD046  -->

### The distribution of the measures for the original ground truths

As for the uniqified ground truths the measures all equal to 1 (theoretically expected, one can verify that on the previous versus figures)

<!-- markdownlint-disable MD046 -->
??? info "Script"

    ```sh title="scripts/uniqify/gt_vs_gt/fig_dist.sh"
    --8<-- "scripts/uniqify/gt_vs_gt/fig_dist.sh"
    ```
<!-- markdownlint-enable MD046 -->

<!--  markdownlint-disable MD046  -->
!!! note "Figure"

    [Distribution](figs/distributions.pdf){ target="_blank" }
<!--  markdownlint-enable MD046  -->