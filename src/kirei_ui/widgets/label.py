from __future__ import annotations

from typing import overload

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from typing_extensions import Self

from kirei_ui.utils import refresh_style


class KireiLabel(QLabel):
    """Static text widget with the KireiUI fluent API.

    Wraps :class:`QLabel`. Setters return ``Self`` so a label can be
    composed inline with alignment, word-wrap, variant and tooltip.
    The base ``kireiRole`` is ``"label"``; :class:`KireiTitle` and
    :class:`KireiText` are thin subclasses that change the role.
    """

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kirei", "label")
        self.setProperty("kireiRole", "label")

    @overload
    def text(self) -> str: ...

    @overload
    def text(self, value: str) -> Self: ...

    def text(self, value: str | None = None) -> str | Self:
        """Get the current text (no arg) or set it (chainable)."""
        if value is None:
            return super().text()
        self.setText(value)
        return self

    def align_center(self) -> Self:
        """Center the text both horizontally and vertically."""
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return self

    def align_left(self) -> Self:
        """Left-align the text, vertically centered."""
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return self

    def align_right(self) -> Self:
        """Right-align the text, vertically centered."""
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return self

    def word_wrap(self, value: bool = True) -> Self:
        """Enable / disable line wrapping when text is wider than the widget."""
        self.setWordWrap(value)
        return self

    def variant(self, name: str) -> Self:
        """Set the ``kireiVariant`` Qt property and re-polish QSS."""
        self.setProperty("kireiVariant", name)
        refresh_style(self)
        return self

    def role(self, name: str) -> Self:
        """Override the ``kireiRole`` Qt property (used by QSS selectors)."""
        self.setProperty("kireiRole", name)
        refresh_style(self)
        return self

    def object_name(self, name: str) -> Self:
        """Set ``QObject.objectName``, useful for ID-targeted QSS rules."""
        self.setObjectName(name)
        return self

    def tooltip(self, value: str) -> Self:
        """Set the hover tooltip text."""
        self.setToolTip(value)
        return self


class KireiTitle(KireiLabel):
    """Heading-style label. Defaults ``kireiRole`` to ``"title"``."""

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kireiRole", "title")


class KireiText(KireiLabel):
    """Body-text label. Defaults ``kireiRole`` to ``"text"``."""

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("kireiRole", "text")
