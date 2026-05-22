from __future__ import annotations

import pytest

pytest.importorskip("PySide6")

from PySide6.QtGui import QIcon

from kirei_ui.icons import KireiIcon, KireiIconRegistry, icon
from kirei_ui.widgets.button import KireiButton
from kirei_ui.widgets.desktop import KireiAction
from kirei_ui.widgets.layout_plus import KireiNavItem


def test_manifest_can_load() -> None:
    names = KireiIconRegistry.names()
    assert isinstance(names, list)


def test_imported_icon_can_be_found() -> None:
    assert KireiIconRegistry.exists("add", style="regular", size=20)


def test_exists_and_path_work() -> None:
    assert KireiIconRegistry.exists("checkmark_circle", style="filled", size=24)
    path = KireiIconRegistry.path("checkmark_circle", style="filled", size=24)
    assert path is not None
    assert path.endswith("checkmark_circle_24_filled.svg")


def test_qicon_factory_returns_qicon() -> None:
    qicon = KireiIcon.qicon("add", style="regular", size=24)
    assert isinstance(qicon, QIcon)


def test_missing_icon_strict_true_raises() -> None:
    with pytest.raises(KeyError):
        KireiIcon.qicon("does_not_exist", strict=True)


def test_missing_icon_strict_false_safe() -> None:
    qicon = icon("does_not_exist", strict=False)
    assert isinstance(qicon, QIcon)


def test_button_navitem_action_icon_api() -> None:
    button = KireiButton("A").icon("add")
    nav = KireiNavItem("B").icon("checkmark_circle", style="filled", size=20)
    action = KireiAction("C").icon("add")
    assert isinstance(button, KireiButton)
    assert isinstance(nav, KireiNavItem)
    assert isinstance(action, KireiAction)
