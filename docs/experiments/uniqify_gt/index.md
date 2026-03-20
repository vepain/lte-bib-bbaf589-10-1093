---
icon: lucide/copy
---

# Analyzing the repeat bias

>[!IMPORTANT]
> Make sure you have installed the `lteu` package, see [Installation](../install.md).

```sh
.
└── 📁 data
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

To run everything in once:

```sh
scripts_dir=scripts/uniqify/gt_vs_gt  # use the correct path (absolute path recommanded)

$scripts_dir/samples.sh
$scripts_dir/uniqify.sh
$scripts_dir/eval_original.sh
$scripts_dir/eval_uniqify.sh
$scripts_dir/fig_vs.sh
$scripts_dir/fig_dist.sh
```

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

```sh
lteu smp repeats samples/complete_hybrid_asm.tsv ground_truths/only_plasmids $exp_dir/samples.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/samples.sh` in the `data` directory.

### Create the uniqify versions of the ground truth bins

For each bin content (only plasmid bins and with chromosomal bin), we create the uniqify versions of the ground truth bins in `📁 gt_vs_gt/ground_truths/only_plasmids` and `📁 gt_vs_gt/ground_truths/with_chromosomes`.

The uniqify versions of the ground truth bins consists in renaming the contigs names such that there is a null contig names intersection between the ground truth bins.

```sh
content=only_plasmids # | with_chromosomes

lteu uniqify gt ground_truths/$content $exp_dir/samples.tsv $exp_dir/ground_truths/$content
```

>[!TIP]
> You can execute the script `scripts/uniqify/gt_vs_gt/uniqify.sh` in the `data` directory.

## Evaluating the completeness and the homogeneity

For each of the ground truths (original and uniqified), we provide the completeness and the homogeneity measures by evaluating the ground truth bins against themselves.

### Original ground truths versus themselves

It creates the files `gt_vs_gt/evals/only_plasmids/original.tsv` and `gt_vs_gt/evals/with_chromosomes/original.tsv`.

```sh
content=only_plasmids # | with_chromosomes
gt_dir=ground_truths/$content

lteu eval run $gt_dir $gt_dir $exp_dir/samples.tsv $exp_dir/evals/$content/original.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/gt_vs_gt/eval_repeats.sh` in the `data` directory.

### Uniqify ground truths versus themselves

It creates the files `gt_vs_gt/evals/only_plasmids/uniqify.tsv` and `gt_vs_gt/evals/with_chromosomess/uniqify.tsv`.

```sh
content=only_plasmids # | with_chromosomes
gt_dir=$exp_dir/ground_truths/$content

lteu eval run $gt_dir $gt_dir $exp_dir/samples.tsv $exp_dir/evals/$content/uniqify.tsv
```

>[!TIP]
> You can execute the script `scripts/uniqify/gt_vs_gt/eval_uniqify.sh` in the `data` directory.
>
## Generating figures

### The versus figure (original ground truths vs uniqified ground truths)

```sh
content=only_plasmids # | with_chromosomes
measure="unw_comp" # | unw_hom | w_comp | w_hom

x_evals_tsv=$exp_dir/evals/$content/original.tsv
x_label="Original"

y_evals_tsv=$exp_dir/evals/$content/uniqify.tsv
y_label="Uniqify"

fig_pdf="$exp_dir/figs/$content/$measure.pdf"

lteu figs vs gt "$measure" "$fig_pdf" \
    --x-axis "$x_evals_tsv" --x-label "$x_label" \
    --y-axis "$y_evals_tsv" --y-label "$y_label"
```

>[!TIP]
> You can execute the script `scripts/uniqify/gt_vs_gt/fig_vs.sh` in the `data` directory.

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

```sh
only_plm_eval_tsv=$exp_dir/evals/only_plasmids/original.tsv
with_chm_eval_tsv=$exp_dir/evals/with_chromosomes/original.tsv

fig_pdf="$exp_dir/figs/distributions.pdf"

lteu figs dist gt "$only_plm_eval_tsv" "$with_chm_eval_tsv" "$fig_pdf"
```

>[!TIP]
> You can execute the script `scripts/uniqify/gt_vs_gt/fig_dist.sh` in the `data` directory.

<!--  markdownlint-disable MD046  -->
??? note "Figure"

    [Distribution](figs/distribution.pdf){ target="_blank" }
<!--  markdownlint-enable MD046  -->