from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QDate, QDateTime, QTime
from PySide6.QtWidgets import QDateEdit, QDateTimeEdit, QTimeEdit, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback


class KireiDateEdit(QDateEdit):
    """Date picker with the KireiUI fluent API.

    Wraps :class:`QDateEdit`. Use :meth:`display_format` for the
    Qt-style format string (e.g. ``"yyyy-MM-dd"``), and
    :meth:`calendar_popup` to opt into the popup calendar.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "date-edit")
        self.setProperty("kireiRole", "datetime")

    def value(self, value: QDate) -> Self:
        """Set the current date. Pair with :meth:`get_value` to read it back."""
        self.setDate(value)
        return self

    def get_value(self) -> QDate:
        """Return the currently displayed :class:`QDate`."""
        return self.date()

    def display_format(self, value: str) -> Self:
        """Set the Qt format string (e.g. ``"yyyy-MM-dd"``)."""
        self.setDisplayFormat(value)
        return self

    def calendar_popup(self, value: bool = True) -> Self:
        """Show / hide the calendar popup arrow next to the field."""
        self.setCalendarPopup(value)
        return self

    def on_change(self, callback: Callable[[QDate], object]) -> Self:
        """Fire when the user picks a different date. Receives the new :class:`QDate`."""
        handler = keep_callback(self, callback)
        self.dateChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the picker."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self


class KireiTimeEdit(QTimeEdit):
    """Time picker with the KireiUI fluent API.

    Wraps :class:`QTimeEdit`. Same chainable shape as
    :class:`KireiDateEdit`, except there is no calendar popup.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "time-edit")
        self.setProperty("kireiRole", "datetime")

    def value(self, value: QTime) -> Self:
        """Set the current time. Pair with :meth:`get_value` to read it back."""
        self.setTime(value)
        return self

    def get_value(self) -> QTime:
        """Return the currently displayed :class:`QTime`."""
        return self.time()

    def display_format(self, value: str) -> Self:
        """Set the Qt format string (e.g. ``"HH:mm:ss"``)."""
        self.setDisplayFormat(value)
        return self

    def on_change(self, callback: Callable[[QTime], object]) -> Self:
        """Fire when the user picks a different time. Receives the new :class:`QTime`."""
        handler = keep_callback(self, callback)
        self.timeChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the picker."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self


class KireiDateTimeEdit(QDateTimeEdit):
    """Combined date + time picker with the KireiUI fluent API.

    Wraps :class:`QDateTimeEdit`. Combines the calendar-popup support
    of :class:`KireiDateEdit` with time-of-day editing.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "datetime-edit")
        self.setProperty("kireiRole", "datetime")

    def value(self, value: QDateTime) -> Self:
        """Set the current datetime. Pair with :meth:`get_value` to read it back."""
        self.setDateTime(value)
        return self

    def get_value(self) -> QDateTime:
        """Return the currently displayed :class:`QDateTime`."""
        return self.dateTime()

    def display_format(self, value: str) -> Self:
        """Set the Qt format string (e.g. ``"yyyy-MM-dd HH:mm"``)."""
        self.setDisplayFormat(value)
        return self

    def calendar_popup(self, value: bool = True) -> Self:
        """Show / hide the calendar popup arrow next to the field."""
        self.setCalendarPopup(value)
        return self

    def on_change(self, callback: Callable[[QDateTime], object]) -> Self:
        """Fire when the user picks a different datetime. Receives the new :class:`QDateTime`."""
        handler = keep_callback(self, callback)
        self.dateTimeChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        """Enable / disable the picker."""
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        """Inverse of :meth:`enabled`."""
        self.setDisabled(value)
        return self
