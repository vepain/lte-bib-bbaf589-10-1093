# To-dos

## Preamble

* Visualize the data
  * [x] Ground truth
  * [x] Predictions

## Formatting task

* [x] Format their ground truth to Plaseval [in `format.py` file](./src/lteu/format.py)
  * [x] Define original ground truth format
  * [x] Define PlasEval ground truth format
* [ ] @vepain Retrieve only sample ID with "Has complete hybrid assembly" set to true in the `Ground-truth` excel sheet
* [ ] @vepain Format binning tools predictions for PlasEval
  * [ ] @vepain Define original format

## Evaluation measures

* [ ] @aniket Homogeneity
* [ ] @aniket Completness

## Chromosomal bin

**Bias:** The measures take into account the bin containing the chromosomal contigs.

* [ ] @vepain Format to PlasEval ground-truth union chromosomal bin

## Repeated contigs

**Bias:** The way they manage the repeated contig does not ensure a perfect prediction has a perfect measure.

* [ ] Identify a subset of the ground truth for which there are repeated contigs
* [ ] Find a measure of repetitiveness to illustrate the bias according to

## Contig lengths

**Bias:** They do not take into account the length of the contigs.

* [ ] Recode the paper V-measure adapted in `lteu/eval.py` (fonction `v_measure`)
* [ ] Adapt the `sklearn` homogeneity and completness measures to take into account the length of the contigs
  * [ ] Code the adapted V-measure in `lteu/eval.py` (fonction `weighted_v_measure`)
