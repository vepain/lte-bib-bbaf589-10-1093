"""Formatting module."""

# Due to typer
# ruff: noqa: FBT002

from pathlib import Path
from typing import Annotated

import pandas as pd
import typer
from rich.panel import Panel

from . import log
from .data import tools
from .data.origin import bins as origin_bins
from .data.origin import gt as origin_gt
from .data.plaseval import bins as pe_bins

APP = typer.Typer(name="fmt", help="Formatting files.")


class GtToPlasEval:
    """Ground-truth to PlasEval args and opts."""

    class Args:
        """Ground-truth to PlasEval args."""

        XLSX_PATH = typer.Argument(
            help="Path to the predictions.xlsx file.",
        )

        OUTPUT_DIR = typer.Argument(
            help="Path to the output directory.",
        )

    class Opts:
        """Ground-truth to PlasEval opts."""

        WITH_CHROMOSOME = typer.Option(
            "--with-chromosome/--without-chromosome",
            help="Format to PlasEval union chromosomal bin.",
        )


@APP.command("gt-to-plaseval")
def gt_to_plaseval(
    xlsx_path: Annotated[Path, GtToPlasEval.Args.XLSX_PATH],
    output_dir: Annotated[Path, GtToPlasEval.Args.OUTPUT_DIR],
    with_chromosome: Annotated[bool, GtToPlasEval.Opts.WITH_CHROMOSOME] = False,
) -> None:
    """Format paper ground truth to PlasEval ground truth."""
    log.CONSOLE.print(
        Panel("[bold]Format paper ground-truth to PlasEval ground truth[/bold]"),
    )
    if with_chromosome:
        log.CONSOLE.print(":microbe: With chromosomal bin")

    output_dir.mkdir(parents=True, exist_ok=True)

    gt_df = origin_gt.to_dataframe(xlsx_path)
    gt_per_smp = gt_df.groupby(origin_gt.Header.SAMPLE_ID)
    count = 0

    def keep_plaseval_and_rename_cols(df: pd.DataFrame) -> pd.DataFrame:
        df = df[
            [
                origin_gt.Header.HYBRID_CTG_ID,
                origin_gt.Header.SR_CTG_ID,
                origin_gt.Header.SR_CTG_LEN,
            ]
        ]
        return df.rename(
            columns={
                origin_gt.Header.HYBRID_CTG_ID: pe_bins.Header.PLASMID,
                origin_gt.Header.SR_CTG_ID: pe_bins.Header.CONTIG,
                origin_gt.Header.SR_CTG_LEN: pe_bins.Header.CTG_LEN,
            },
        )

    for smp_id, smp_df in gt_per_smp:
        plm_smp_df: pd.DataFrame = smp_df[
            smp_df[origin_gt.Header.GT_CLASS] == "plasmid"
        ]

        plaseval_gt_df = keep_plaseval_and_rename_cols(plm_smp_df)

        if with_chromosome:  # i.e. with_chromosome
            chr_smp_df: pd.DataFrame = smp_df[
                smp_df[origin_gt.Header.GT_CLASS] == "chromosome"
            ]
            chr_smp_df = keep_plaseval_and_rename_cols(chr_smp_df)
            chr_smp_df[pe_bins.Header.PLASMID] = "C1"

            # Add rows of chr_smp_df after rows of plaseval_gt_df
            plaseval_gt_df = pd.concat(
                [plaseval_gt_df, chr_smp_df],
                ignore_index=True,
            )

        plaseval_gt_df.to_csv(output_dir / f"{smp_id}.tsv", sep="\t", index=False)
        count += 1

    log.CONSOLE.print(
        ":white_check_mark:"
        f" [green]Created {count} files in"
        f" :file_folder: [bold]{output_dir}[/bold] directory[/green]",
    )


class CompleteHybridAsm:
    """Complete hybrid assembly args and opts."""

    class Args:
        """Complete hybrid assembly args."""

        XLSX_PATH = typer.Argument(
            help="Path to the predictions.xlsx file.",
        )

        TSV_OUTPUT = typer.Argument(
            help="Path to the output TSV file.",
        )


@APP.command("complete-hybrid-asm")
def extract_complete_assembly(
    xlsx_path: Annotated[Path, CompleteHybridAsm.Args.XLSX_PATH],
    tsv_output: Annotated[Path, CompleteHybridAsm.Args.TSV_OUTPUT],
) -> None:
    """Extract complete hybrid assemblies."""
    log.CONSOLE.print(
        Panel("[bold]Extract complete hybrid assemblies[/bold]"),
    )
    tsv_output.parent.mkdir(parents=True, exist_ok=True)

    gt_df = origin_gt.to_dataframe(xlsx_path)
    gt_df = gt_df[gt_df[origin_gt.Header.HAS_COMPLETE_HYBRID_ASM]]

    gt_df[gt_df[origin_gt.Header.SAMPLE_ID].duplicated(keep=False)][
        origin_gt.Header.SAMPLE_ID
    ].to_csv(
        tsv_output,
        sep="\t",
        index=False,
    )

    log.CONSOLE.print(
        ":white_check_mark:"
        f" [green]Created :page_facing_up: [bold]{tsv_output}[/bold] file[/green]",
    )


class BinToPlasEval:
    """Plasmid reconstruction to PlasEval args and opts."""

    class Args:
        """Plasmid reconstruction to PlasEval args."""

        XLSX_PATH = typer.Argument(
            help="Path to the predictions.xlsx file.",
        )

        OUTPUT_DIR = typer.Argument(
            help="Path to the output directory.",
        )

        TOOL = typer.Argument(
            help="Binning tool code.",
        )

    class Opts:
        """Plasmid reconstruction to PlasEval opts."""

        WITH_CHROMOSOME = typer.Option(
            "--with-chromosome/--without-chromosome",
            help="Format to PlasEval union chromosomal bin.",
        )


@APP.command("bins-to-plaseval")
def bins_to_plaseval(
    xlsx_path: Annotated[Path, BinToPlasEval.Args.XLSX_PATH],
    tool: Annotated[tools.Binning, BinToPlasEval.Args.TOOL],
    output_dir: Annotated[Path, BinToPlasEval.Args.OUTPUT_DIR],
    with_chromosome: Annotated[bool, BinToPlasEval.Opts.WITH_CHROMOSOME] = False,
) -> None:
    """Format paper bins to PlasEval bins."""
    log.CONSOLE.print(
        Panel("[bold]Format paper bins to PlasEval bins[/bold]"),
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    tool_col = origin_bins.binning_tool_to_header(tool)

    bins_per_smp_df = origin_bins.to_dataframe(xlsx_path)[
        [origin_bins.Header.SAMPLE_ID, origin_bins.Header.SR_CTG_ID, tool_col]
    ].groupby(origin_bins.Header.SAMPLE_ID)

    gt_per_smp_df = origin_gt.to_dataframe(xlsx_path).groupby(
        origin_gt.Header.SAMPLE_ID,
    )

    def keep_plaseval_and_rename_cols(df: pd.DataFrame) -> pd.DataFrame:
        return df[
            [
                tool_col,
                origin_bins.Header.SR_CTG_ID,
            ]
        ].rename(
            columns={
                tool_col: pe_bins.Header.PLASMID,
                origin_bins.Header.SR_CTG_ID: pe_bins.Header.CONTIG,
            },
        )

    count = 0
    no_bins_count = 0
    for smp_id, smp_df in bins_per_smp_df:
        if not with_chromosome:
            smp_df = smp_df[smp_df[tool_col] != "chromosome"]  # noqa: PLW2901
        if tool == tools.Binning.GPLAS_TWO:
            smp_df = smp_df[~smp_df[tool_col].str.contains("Unbinned")]  # noqa: PLW2901

        if smp_df[tool_col].isna().any():  # no bins
            no_bins_count += 1
            continue

        plaseval_bins_df = keep_plaseval_and_rename_cols(smp_df)

        gt_smp = gt_per_smp_df.get_group(smp_id).rename(
            columns={
                origin_gt.Header.SR_CTG_ID: pe_bins.Header.CONTIG,
                origin_gt.Header.SR_CTG_LEN: pe_bins.Header.CTG_LEN,
            },
        )
        #
        # Add the contig length column
        #
        plaseval_bins_df = plaseval_bins_df.merge(
            gt_smp[[pe_bins.Header.CONTIG, pe_bins.Header.CTG_LEN]],
            how="left",
            on=pe_bins.Header.CONTIG,
        )
        #
        # Duplicate contigs when they belong to several bins
        #
        several_bins_rows = plaseval_bins_df[
            plaseval_bins_df[pe_bins.Header.PLASMID].str.contains(";")
        ]
        plaseval_bins_df = plaseval_bins_df[
            ~plaseval_bins_df[pe_bins.Header.PLASMID].str.contains(";")
        ]
        for _, row in several_bins_rows.iterrows():
            for bin_id in row[pe_bins.Header.PLASMID].split(";"):
                new_row = row.copy()
                new_row[pe_bins.Header.PLASMID] = bin_id
                plaseval_bins_df = pd.concat(
                    [plaseval_bins_df, new_row.to_frame().T],
                    ignore_index=True,
                )

        plaseval_bins_df.to_csv(
            output_dir / f"{smp_id}.tsv",
            sep="\t",
            index=False,
        )

        count += 1

    log.CONSOLE.print(
        ":white_check_mark:"
        f" [green]Created {count} files in"
        f" :file_folder: [bold]{output_dir}[/bold] directory[/green]",
    )
    if no_bins_count:
        log.CONSOLE.print(
            f":warning: [yellow]No bins for {no_bins_count} samples[/yellow]",
        )
