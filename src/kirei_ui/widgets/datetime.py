from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QDate, QDateTime, QTime
from PySide6.QtWidgets import QDateEdit, QDateTimeEdit, QTimeEdit, QWidget
from typing_extensions import Self

from kirei_ui.utils import keep_callback


class KireiDateEdit(QDateEdit):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "date-edit")
        self.setProperty("kireiRole", "datetime")

    def value(self, value: QDate) -> Self:
        self.setDate(value)
        return self

    def get_value(self) -> QDate:
        return self.date()

    def display_format(self, value: str) -> Self:
        self.setDisplayFormat(value)
        return self

    def calendar_popup(self, value: bool = True) -> Self:
        self.setCalendarPopup(value)
        return self

    def on_change(self, callback: Callable[[QDate], object]) -> Self:
        handler = keep_callback(self, callback)
        self.dateChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self


class KireiTimeEdit(QTimeEdit):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "time-edit")
        self.setProperty("kireiRole", "datetime")

    def value(self, value: QTime) -> Self:
        self.setTime(value)
        return self

    def get_value(self) -> QTime:
        return self.time()

    def display_format(self, value: str) -> Self:
        self.setDisplayFormat(value)
        return self

    def on_change(self, callback: Callable[[QTime], object]) -> Self:
        handler = keep_callback(self, callback)
        self.timeChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self


class KireiDateTimeEdit(QDateTimeEdit):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("kirei", "datetime-edit")
        self.setProperty("kireiRole", "datetime")

    def value(self, value: QDateTime) -> Self:
        self.setDateTime(value)
        return self

    def get_value(self) -> QDateTime:
        return self.dateTime()

    def display_format(self, value: str) -> Self:
        self.setDisplayFormat(value)
        return self

    def calendar_popup(self, value: bool = True) -> Self:
        self.setCalendarPopup(value)
        return self

    def on_change(self, callback: Callable[[QDateTime], object]) -> Self:
        handler = keep_callback(self, callback)
        self.dateTimeChanged.connect(handler)
        return self

    def enabled(self, value: bool = True) -> Self:
        self.setEnabled(value)
        return self

    def disabled(self, value: bool = True) -> Self:
        self.setDisabled(value)
        return self
