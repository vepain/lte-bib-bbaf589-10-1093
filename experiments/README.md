# Experiment

> [!NOTE]
> The experiments description concerns the run on the `Fir` Alliance Canada cluster.
> In order to share the files, make sure to configurate the `umask`: `umask 007`.

## Fir file structure

In `/project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor` directory.

```sh
.
├── data
│   ├── samples
│   │   └── complete_hybrid_asm.tsv
│   ├── original  # Original data
│   │   └── predictions.xlsx
│   ├── ground_truths  # PlasEval formatted ground-truths
│   │   ├── only_plasmids
│   │   └── with_chromosomes
│   ├── binning  # PlasEval formatted bins
│   │   ├── only_plasmids
│   │   │   └── $tool
│   │   └── with_chromosomes  # Same subtree as only_plasmids/
│   ├── uniqify  # Predictions and ground-truths after uniqify
│   │   ├── only_plasmids
│   │   │   └── $tool
│   │   │       ├── predictions # one file per sample
│   │   │       ├── ground_truths # idem
│   │   │       └── nb_matches.tsv
│   │   └── with_chromosomes # Same subtree as only_plasmids/
│   ├── comp_hom  # Completeness and homogeneity
│   │   ├── only_plasmids
│   │   │   ├── repeats
│   │   │   │   └── $tool.tsv
│   │   │   └── uniqify # Same subtree as repeats/
│   │   └── with_chromosomes # Same subtree as only_plasmids/
│   └── plaseval  # PlasEval results
│       ├── only_plasmids
│       │   └──comp  # comp subcommand
│       │      └── alpha_05  # For alpha = 0.5
│       │          └── $tool
│       └── with_chromosomes # Same subtree as only_plasmids/
├── scripts  # SBATCH scripts
└── tools  # Tools cloned repositories
```

Two variables:

```sh
content="only_plasmids"  # or "with_chromosomes"
tool="gplas2"  # or "hyasp" or "mob" or "pbf"
#
# Path structure
#
data_dir="data"
original_xlsx="$data_dir/original/predictions.xlsx"
gt_dir="$data_dir/ground_truth/$content"
bin_dir="$data_dir/binning/$content/$tool"
plaseval_comp_dir="$data_dir/plaseval/comp/$content/$tool"
```

### Initialize the data

The following commands are run on fir.

Data:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor
mkdir -p data/original
wget https://github.com/broadinstitute/plasmid-detection-benchmark/raw/main/data/predictions.xlsx -O data/original/predictions.xlsx
```

Tools:

>[!WARNING]
> Make sure you have added your SSH key to get access to the repository.
>
> 1. Create a new SSH key in Fir, linked to your GitHub account (see [GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key))
> 2. Start the SSH agent: `eval "$(ssh-agent -s)"`
> 3. Add your SSH key: `ssh-add ~/.ssh/your_key_id`

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor
mkdir tools
cd tools
git clone -b develop git@github.com:vepain/lte-bib-bbaf589-10-1093.git
```

### Help on installing the virual environment

#### `lteu`

```sh
# Create a test directory
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor
mkdir tmp
cd tmp
# ---
git clone -b develop git@github.com:vepain/lte-bib-bbaf589-10-1093.git
cd lte-bib-bbaf589-10-1093
module load python/3.13
virtualenv --no-download .venv
source .venv/bin/activate
pip install uv-build
pip install .
```

## Get the list of samples with complete hybrid assemblies

### installation

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor
mkdir -p scripts/samples
```

From here:

```sh
scp ./scripts/samples/complete_hybrid_asm.sh fir:/project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/samples
```

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/samples
chmod ug+rwx complete_hybrid_asm.sh
```

### Usage

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/samples
sbatch complete_hybrid_asm.sh
```

## Format the ground truth to the PlasEval format

With and without the chromosomal bin.

C.f. `./scripts/fmt_to_plaseval/ground_truth.sh`

### installation

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor
mkdir -p scripts/fmt_to_plaseval
```

From here:

```sh
scp ./scripts/fmt_to_plaseval/ground_truth.sh fir:/project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/fmt_to_plaseval
```

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/fmt_to_plaseval
chmod ug+rwx ground_truth.sh
```

### Usage

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/fmt_to_plaseval
sbatch ground_truth.sh
```

## Format the bins to the PlasEval format

With and without the chromosomal bin.

C.f. `./scripts/fmt_to_plaseval/bins.sh`

### installation

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor
mkdir -p scripts/fmt_to_plaseval
```

From here:

```sh
scp ./scripts/fmt_to_plaseval/bins.sh fir:/project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/fmt_to_plaseval
```

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/fmt_to_plaseval
chmod ug+rwx bins.sh
```

### Usage

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/fmt_to_plaseval
sbatch bins.sh
```

## Running PlasEval comp on samples with complete hybrid assemblies

With or without the chromosomal bin, for one given method.

C.f. `./scripts/plaseval/comp.sh`

### installation

#### Install PlasEval

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/tools
git clone git@github.com:vepain/PlasEval.git
```

#### Set the sbatch script

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor
mkdir -p scripts/plaseval
```

From here:

```sh
scp ./scripts/plaseval/comp.sh fir:/project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/plaseval
```

On fir:

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/plaseval
chmod ug+rwx comp.sh
```

### Usage

```sh
cd /project/def-chauvec/wg-anoph/benchmarking/2026_letter_to_editor/scripts/plaseval
sbatch comp.sh
```

## Distinguishing the repeats

To answer the repeat bias

<!-- TODO CONTINUE HERE -->