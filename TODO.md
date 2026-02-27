# To-dos

## Preamble

* Visualize the data
  * [ ] Ground truth
  * [ ] Predictions

## Formatting task

* [ ] Format their ground truth to Plaseval [in `format.py` file](./src/lteu/format.py)
  * [ ] Define original ground truth format
  * [ ] Define PlasEval ground truth format
* [ ] Retrieve only sample ID with "Has complete hybrid assembly" set to true in the `Ground-truth` excel sheet

## Chromosomal bin

**Bias:** The measures take into account the bin containing the chromosomal contigs.

## Repeated contigs

**Bias:** The way they manage the repeated contig does not ensure a perfect prediction has a perfect measure.

* [ ] Identify a subset of the ground truth for which there are repeated contigs
* [ ] Find a measure of repetitiveness to illustrate the bias according to

## Contig lengths

**Bias:** They do not take into account the length of the contigs.

* [ ] Recode the paper V-measure adapted in `lteu/eval.py` (fonction `v_measure`)
* [ ] Adapt the `sklearn` homogeneity and completness measures to take into account the length of the contigs
  * [ ] Code the adapted V-measure in `lteu/eval.py` (fonction `weighted_v_measure`)
