"""Formatting module."""

# Due to typer
# ruff: noqa: FBT002

from pathlib import Path
from typing import Annotated

import pandas as pd
import typer

from lteu import log, tools
from lteu.origin import bins as origin_bins
from lteu.origin import gt as origin_gt
from lteu.plaseval import bins as pe_bins

APP = typer.Typer()


class GroundTruthsInputs:
    """Ground-truth to PlasEval args and opts."""

    XLSX_PATH = typer.Argument(
        help="Path to the predictions.xlsx file.",
    )

    OUTPUT_DIR = typer.Argument(
        help="Path to the output directory.",
    )
    WITH_CHROMOSOMES = typer.Option(
        "--with-chromosomes/--without-chromosomes",
        help="Format to PlasEval union chromosomal bin.",
    )


@APP.command("ground-truths")
def gt_to_plaseval(
    xlsx_path: Annotated[Path, GroundTruthsInputs.XLSX_PATH],
    output_dir: Annotated[Path, GroundTruthsInputs.OUTPUT_DIR],
    with_chromosomes: Annotated[bool, GroundTruthsInputs.WITH_CHROMOSOMES] = False,
) -> None:
    """Format paper ground truth bins to PlasEval ground truths."""
    log.print_title("Format paper ground-truth bins to PlasEval ground truths")

    log.print_inputs(
        (
            f"XLSX file: {log.fmt_file(xlsx_path)}",
            f"Output directory: {log.fmt_dir(output_dir)}",
            log.fmt_with_chr_input(with_chromosomes),
        ),
    )

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

    smp_id: str
    for smp_id, smp_df in gt_per_smp:  # ty:ignore[invalid-assignment]
        plm_smp_df: pd.DataFrame = smp_df[
            smp_df[origin_gt.Header.GT_CLASS] == "plasmid"
        ]

        plaseval_gt_df = keep_plaseval_and_rename_cols(plm_smp_df)

        if with_chromosomes:  # i.e. with_chromosomes
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

        #
        # Duplicate contigs when they belong to several bins
        #
        several_bins_rows = plaseval_gt_df[
            plaseval_gt_df[pe_bins.Header.PLASMID].str.contains(";")
        ]
        plaseval_gt_df = plaseval_gt_df.drop(several_bins_rows.index)
        for _, row in several_bins_rows.iterrows():
            for bin_id in row[pe_bins.Header.PLASMID].split(";"):
                new_row = row.copy()
                new_row[pe_bins.Header.PLASMID] = bin_id
                plaseval_gt_df = pd.concat(
                    [plaseval_gt_df, new_row.to_frame().T],
                    ignore_index=True,
                )

        plaseval_gt_df.to_csv(output_dir / pe_bins.fname(smp_id), sep="\t", index=False)
        count += 1

    log.print_done(f"Created {count} files in {log.fmt_dir(output_dir)} directory")


class BinsInputs:
    """Plasmid reconstruction to PlasEval args and opts."""

    XLSX_PATH = typer.Argument(
        help="Path to the predictions.xlsx file.",
    )

    OUTPUT_DIR = typer.Argument(
        help="Path to the output directory.",
    )

    TOOL = typer.Argument(
        help="Binning tool code.",
    )

    WITH_CHROMOSOMES = typer.Option(
        "--with-chromosomes/--without-chromosomes",
        help="Format to PlasEval union chromosomal bin.",
    )


@APP.command("bins")
def bins_to_plaseval(
    xlsx_path: Annotated[Path, BinsInputs.XLSX_PATH],
    tool: Annotated[tools.Binning, BinsInputs.TOOL],
    output_dir: Annotated[Path, BinsInputs.OUTPUT_DIR],
    with_chromosomes: Annotated[bool, BinsInputs.WITH_CHROMOSOMES] = False,
) -> None:
    """Format paper bins to PlasEval bins."""
    log.print_title("Format paper bins to PlasEval bins")

    log.print_inputs(
        (
            f"XLSX file: {log.fmt_file(xlsx_path)}",
            f"Binning tool: {log.fmt_tool(tool)}",
            f"Output directory: {log.fmt_dir(output_dir)}",
            log.fmt_with_chr_input(with_chromosomes),
        ),
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
    smp_id: str
    for smp_id, smp_df in bins_per_smp_df:  # ty:ignore[invalid-assignment]
        if smp_df[tool_col].isna().any():  # no bins
            no_bins_count += 1
            continue

        if tool == tools.Binning.GPLAS_TWO:
            if not with_chromosomes:
                smp_df = smp_df[~smp_df[tool_col].str.contains("Unbinned")]  # noqa: PLW2901
            else:
                smp_df.loc[
                    smp_df[tool_col].str.contains("Unbinned"),
                    tool_col,
                ] = "chromosome"

        if not with_chromosomes:
            smp_df = smp_df[smp_df[tool_col] != "chromosome"]  # noqa: PLW2901

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
        plaseval_bins_df = plaseval_bins_df.drop(several_bins_rows.index)
        for _, row in several_bins_rows.iterrows():
            for bin_id in row[pe_bins.Header.PLASMID].split(";"):
                new_row = row.copy()
                new_row[pe_bins.Header.PLASMID] = bin_id
                plaseval_bins_df = pd.concat(
                    [plaseval_bins_df, new_row.to_frame().T],
                    ignore_index=True,
                )

        plaseval_bins_df.to_csv(
            output_dir / pe_bins.fname(smp_id),
            sep="\t",
            index=False,
        )

        count += 1

    log.print_done(
        f"Created {count} files in {log.fmt_dir(output_dir)} directory",
    )
    if no_bins_count:
        log.print_warning(f"No results for {no_bins_count} samples")
