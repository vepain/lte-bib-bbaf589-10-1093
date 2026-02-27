"""Formatting module."""

from pathlib import Path
from typing import Annotated

import pandas as pd
import typer
from rich import print as rprint

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


@APP.command("gt-to-plaseval")
def gt_to_plaseval(
    xlsx_path: Annotated[Path, GtToPlasEval.Args.XLSX_PATH],
    output_dir: Annotated[Path, GtToPlasEval.Args.OUTPUT_DIR],
) -> None:
    """Format paper ground truth to PlasEval ground truth."""
    rprint("[blue]Formatting ground-truth for PlasEval[/blue]")

    output_dir.mkdir(parents=True, exist_ok=True)

    gt_df = origin_gt.to_dataframe(xlsx_path)
    gt_per_smp = gt_df.groupby(origin_gt.Header.SAMPLE_ID)
    count = 0
    for smp_id, smp_df in gt_per_smp:
        plm_smp_df: pd.DataFrame = smp_df[
            smp_df[origin_gt.Header.GT_CLASS] == "plasmid"
        ]
        plaseval_gt_df = plm_smp_df.rename(
            columns={
                origin_gt.Header.HYBRID_CTG_ID: pe_bins.Header.PLASMID,
                origin_gt.Header.SR_CTG_ID: pe_bins.Header.CONTIG,
                origin_gt.Header.SR_CTG_LEN: pe_bins.Header.CTG_LEN,
            },
        )
        plaseval_gt_df = plaseval_gt_df[
            [
                pe_bins.Header.PLASMID,
                pe_bins.Header.CONTIG,
                pe_bins.Header.CTG_LEN,
            ]
        ]
        plaseval_gt_df.to_csv(output_dir / f"{smp_id}.tsv", sep="\t", index=False)
        count += 1
    rprint(
        ":white_check_mark:"
        f" [green]Created {count} files in {output_dir} directory[/green]",
    )
