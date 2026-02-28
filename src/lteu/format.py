"""Formatting module."""

# Due to typer
# ruff: noqa: FBT002

from pathlib import Path
from typing import Annotated

import pandas as pd
import typer
from rich.panel import Panel

from . import log
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
    # Use rich print to print a beautiful title in CONSOLE without markdown
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
    # Keep only colum Sample ID with unique value
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
