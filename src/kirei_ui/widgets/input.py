from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QLineEdit, QTextEdit, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback


class KireiInput(QLineEdit):
    """Single-line text input with the KireiUI fluent API.

    Wraps :class:`QLineEdit` with chainable configuration methods. Setters
    return ``Self`` so a control can be built in one expression:

        >>> name = (
        ...     KireiInput()
        ...     .placeholder("Username")
        ...     .clearable()
        ...     .max_length(32)
        ...     .on_change(lambda v: print(v))
        ... )

    The native ``textChanged`` / ``returnPressed`` signals still work; the
    ``on_change`` and ``on_submit`` helpers are convenience wrappers that
    keep the underlying handler alive on the widget so PySide6 will not
    garbage-collect short-lived closures.

    QSS hooks: ``kirei="input"``, ``kireiRole="input"``.
    """

    def __init__(self, value: str = "", parent: QWidget | None = None) -> None:
        """Create the input.

        Args:
            value: Initial text. Use ``""`` to start empty.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setProperty("kirei", "input")
        self.setProperty("kireiRole", "input")
        if value:
            self.setText(value)

    def placeholder(self, value: str) -> Self:
        """Set the greyed placeholder shown when the field is empty."""
        self.setPlaceholderText(value)
        return self

    def value(self, value: str) -> Self:
        """Set the current text. Pair with :meth:`get_value` to read it back."""
        self.setText(value)
        return self

    def get_value(self) -> str:
        """Return the current text."""
        return self.text()

    def clearable(self, value: bool = True) -> Self:
        """Show / hide a built-in clear button at the right edge of the field."""
        self.setClearButtonEnabled(value)
        return self

    def readonly(self, value: bool = True) -> Self:
        """Toggle read-only mode. Read-only fields still receive focus."""
        self.setReadOnly(value)
        return self

    def max_length(self, value: int) -> Self:
        """Cap the maximum number of characters the user may type."""
        self.setMaxLength(value)
        return self

    def on_change(self, callback: Callable[[str], object]) -> Self:
        """Fire on every character change. Receives the full current text."""
        handler = keep_callback(self, callback)
        self.textChanged.connect(handler)
        return self

    def on_submit(self, callback: Callable[[], object]) -> Self:
        """Fire when the user presses Enter / Return. No arguments passed."""
        def handler() -> object:
            return callback()

        saved = keep_callback(self, handler)
        self.returnPressed.connect(saved)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable or disable the input."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self


class KireiPassword(KireiInput):
    """Password variant of :class:`KireiInput`.

    Echo mode defaults to ``QLineEdit.EchoMode.Password``. Use
    :meth:`show_password` to toggle visibility on a "show password" button.
    """

    def __init__(self, value: str = "", parent: QWidget | None = None) -> None:
        super().__init__(value=value, parent=parent)
        self.setProperty("kireiRole", "password")
        self.setEchoMode(QLineEdit.EchoMode.Password)

    def show_password(self, value: bool = True) -> Self:
        """Show plain text when ``value`` is True; hide it again when False."""
        mode = QLineEdit.EchoMode.Normal if value else QLineEdit.EchoMode.Password
        self.setEchoMode(mode)
        return self


class KireiTextarea(QTextEdit):
    """Multi-line text input with the KireiUI fluent API.

    Wraps :class:`QTextEdit`. Same chainable shape as :class:`KireiInput`,
    but ``on_change`` does not receive the new text (Qt's ``textChanged``
    on QTextEdit emits no payload — call :meth:`get_value` from the
    handler if needed).
    """

    def __init__(self, value: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "textarea")
        self.setProperty("kireiRole", "textarea")
        if value:
            self.setPlainText(value)

    def placeholder(self, value: str) -> Self:
        self.setPlaceholderText(value)
        return self

    def value(self, value: str) -> Self:
        self.setPlainText(value)
        return self

    def get_value(self) -> str:
        return self.toPlainText()

    def readonly(self, value: bool = True) -> Self:
        self.setReadOnly(value)
        return self

    def on_change(self, callback: Callable[[], object]) -> Self:
        """Fire on every change. Receives no arguments — read via :meth:`get_value`."""
        handler = keep_callback(self, callback)
        self.textChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self
