# To-dos

## Preamble

* Visualize the data
  * [x] Ground truth
  * [x] Predictions

## Formatting task

* [x] Format their ground truth to Plaseval [in `format.py` file](./src/lteu/format.py)
  * [x] Define original ground truth format
  * [x] Define PlasEval ground truth format
* [ ] @vepain Retrieve only sample ID with "Has complete hybrid assembly" set to true in the `Ground-truth` Excel sheet
* [ ] @vepain Format binning tools predictions for PlasEval
  * [ ] @vepain Define original format

## Evaluation measures

* [ ] @aniket Homogeneity
* [ ] @aniket Completeness

## Chromosomal bin

**Bias:** The measures take into account the bin containing the chromosomal contigs.

* [x] @vepain Format to PlasEval ground-truth union chromosomal bin

## Repeated contigs

**Bias:** The way they manage the repeated contig does not ensure a perfect prediction has a perfect measure.

* [ ] Identify a subset of the ground truth for which there are repeated contigs
* [ ] Find a measure of repetitiveness to illustrate the bias according to

## Contig lengths

**Bias:** They do not take into account the length of the contigs.

## Running

On Fir Alliance Canada cluster.

On samples with complete hybrid assemblies.

### Formatting tasks

* Data for PlasEval format
  * [x] ground truths
  * [x] bins
* [x] samples with complete hybrid assemblies

### PlasEval

* Only plasmids
  * [x] hyasp
  * [x] gplas2
  * [x] pbf
  * [x] mob
* [ ] With chromosome?

### Original homogeneity and completeness measures

* Only plasmids
  * [ ] hyasp
  * [ ] gplas2
  * [ ] pbf
  * [ ] mob
* With chromosome
  * [ ] hyasp
  * [ ] gplas2
  * [ ] pbf
  * [ ] mob
