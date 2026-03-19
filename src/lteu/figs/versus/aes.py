"""Sommon versus aesthetics."""

from lteu.figs import aes


class Labels:
    """Labels for a versus figure."""

    def __init__(
        self,
        title: str,
        x_label: str,
        y_label: str,
    ) -> None:
        self._title: str = title
        self._x_label: str = x_label
        self._y_label: str = y_label

    def title(self) -> str:
        """Get title."""
        return self._title

    def x(self) -> str:
        """Get x label."""
        return self._x_label

    def y(self) -> str:
        """Get y label."""
        return self._y_label


class Config:
    """Aeshetics for a versus figure."""

    def __init__(
        self,
        base_cfg: aes.Base,
        labels: Labels,
    ) -> None:
        self._base_cfg: aes.Base = base_cfg
        self._labels: Labels = labels

    def base(self) -> aes.Base:
        """Get the base configuration."""
        return self._base_cfg

    def labels(self) -> Labels:
        """Get the labels configuration."""
        return self._labels
