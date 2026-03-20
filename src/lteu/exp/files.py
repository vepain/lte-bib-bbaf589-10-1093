"""Experiments common files."""

from pathlib import Path

from lteu import bins, tools


class Original:
    """Original data file system."""

    ORIGINAL_DIRNAME = Path("original")

    PREDICTIONS_FILENAME = Path("predictions.xlsx")

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir

    def data_dir(self) -> Path:
        """Get data directory."""
        return self._data_dir

    def dir(self) -> Path:
        """Get original directory."""
        return self._data_dir / self.ORIGINAL_DIRNAME

    def predictions_xlsx(self) -> Path:
        """Get predictions Excel file."""
        return self.dir() / self.PREDICTIONS_FILENAME


class Samples:
    """Experiments samples file system."""

    SAMPLE_DIRNAME = Path("samples")

    COMPLETE_HYBRID_ASM_FILENAME = Path("complete_hybrid_asm.tsv")

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir

    def data_dir(self) -> Path:
        """Get data directory."""
        return self._data_dir

    def dir(self) -> Path:
        """Get samples directory."""
        return self._data_dir / self.SAMPLE_DIRNAME

    def complete_hybrid_asm_tsv(self) -> Path:
        """Get complete hybrid assemblies TSV file."""
        return self.dir() / self.COMPLETE_HYBRID_ASM_FILENAME


class GroundTruths:
    """Experiments ground truths file system."""

    GROUND_TRUTHS_DIRNAME = Path("ground_truths")

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir

    def data_dir(self) -> Path:
        """Get data directory."""
        return self._data_dir

    def dir(self) -> Path:
        """Get ground truths directory."""
        return self._data_dir / self.GROUND_TRUTHS_DIRNAME

    def only_plasmids_dir(self) -> Path:
        """Get only plasmids directory."""
        return self.content_dir(bins.Contents.ONLY_PLASMIDS)

    def with_chromosomes_dir(self) -> Path:
        """Get with chromosomes directory."""
        return self.content_dir(bins.Contents.WITH_CHROMOSOMES)

    def content_dir(self, content: bins.Contents) -> Path:
        """Get content directory."""
        return self.dir() / content


class Binning:
    """Experiments binning file system."""

    BINNING_DIRNAME = Path("binning")

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir

    def data_dir(self) -> Path:
        """Get data directory."""
        return self._data_dir

    def dir(self) -> Path:
        """Get binning directory."""
        return self._data_dir / self.BINNING_DIRNAME

    def only_plasmids_dir(self) -> Path:
        """Get only plasmids directory."""
        return self.content_dir(bins.Contents.ONLY_PLASMIDS)

    def with_chromosomes_dir(self) -> Path:
        """Get with chromosomes directory."""
        return self.content_dir(bins.Contents.WITH_CHROMOSOMES)

    def content_dir(self, content: bins.Contents) -> Path:
        """Get content directory."""
        return self.dir() / content

    def tool_dir(
        self,
        content: bins.Contents,
        tool_code: tools.Binning,
    ) -> Path:
        """Get tool directory."""
        return self.content_dir(content) / tool_code
