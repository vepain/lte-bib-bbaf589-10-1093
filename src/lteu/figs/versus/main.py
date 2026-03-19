"""Versus figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from . import aes, data


def gt(
    df: pd.DataFrame,
    aes_cfg: aes.Config,
    class_col: str,
    pdf_path: Path,
) -> None:
    """Create a versus figure for ground truths."""
    sns.set_context(aes_cfg.base().context())  # ty:ignore[invalid-argument-type]

    fig, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(
        data=df,
        x=data.Versions.V1,
        y=data.Versions.V2,
        hue=class_col,
        hue_order=[data.Class.ABOVE, data.Class.EQUAL, data.Class.BELOW],
        palette="Set3",
        ax=ax,
        zorder=2,
    )

    def final_aes() -> None:
        #
        # Add diagonal in background
        #
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        lims = [max(x0, y0), min(x1, y1)]
        ax.plot(
            lims,
            lims,
            color="grey",
            linewidth=1,
            linestyle="-",
            alpha=0.8,
            zorder=1,
        )
        #
        # Legends
        #
        ax.set_title("" if aes_cfg.base().focus() else f"{aes_cfg.labels().title()}")

        ax.set_xlabel(f"{aes_cfg.labels().x()}\n(n = {df.shape[0]})")
        ax.set_ylabel(aes_cfg.labels().y())

    final_aes()

    fig.savefig(pdf_path)
    plt.close()
