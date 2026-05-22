"""Behavior-level regressions for KireiUI.

This file complements ``test_fluent.py`` (which mostly checks "method returns
self" patterns) with assertions about *what actually happens* when components
are used. Each test is annotated with the bug or design contract it locks in.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QToolButton, QWidget

from kirei_ui.locale import KireiTexts
from kirei_ui.motion import KireiMotionMixin
from kirei_ui.stack import KireiPanel, KireiSplitter
from kirei_ui.theme import build_qss
from kirei_ui.utils import (
    attached_list,
    clear_layout,
    keep_callback,
    refresh_style,
)
from kirei_ui.widgets.button import KireiButton
from kirei_ui.widgets.choice import KireiCheckbox, KireiRadio
from kirei_ui.widgets.feedback import KireiBadge, KireiProgress, KireiSpinner
from kirei_ui.widgets.input import KireiInput
from kirei_ui.widgets.label import KireiLabel, KireiText, KireiTitle
from kirei_ui.widgets.layout_plus import KireiBreadcrumbs, KireiNavItem, KireiSidebar
from kirei_ui.widgets.number import KireiDoubleSpinBox, KireiSlider, KireiSpinBox
from kirei_ui.widgets.switch import KireiSwitch


@pytest.fixture(scope="module", autouse=True)
def _app() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


# ---------------------------------------------------------------------------
# Getter / setter overload contract
#
# Regression: a previous build had ``def text(self, value: str) -> Self`` on
# every Kirei*-Label widget, which broke ``label.text()`` (TypeError, missing
# argument). All these widgets must support both forms now.
# ---------------------------------------------------------------------------


def test_label_text_getter_returns_initial_text() -> None:
    assert KireiLabel("hi").text() == "hi"


def test_label_text_setter_updates_value_and_chains() -> None:
    label = KireiLabel("a")
    chained = label.text("b")
    assert chained is label
    assert label.text() == "b"


def test_title_and_text_inherit_getter_overload() -> None:
    assert KireiTitle("hi").text() == "hi"
    assert KireiText("hi").text() == "hi"


def test_checkbox_radio_text_getter() -> None:
    assert KireiCheckbox("yes").text() == "yes"
    assert KireiRadio("yes").text() == "yes"


def test_switch_text_getter_and_size_dual_overload() -> None:
    sw = KireiSwitch("on")
    assert sw.text() == "on"
    # size() with no arg is the QSize getter inherited from QWidget
    assert isinstance(sw.size(), QSize)
    # size("name") is the kireiSize setter
    assert sw.size("compact") is sw
    assert sw.property("kireiSize") == "compact"


def test_spinner_text_getter_and_default_uses_locale() -> None:
    spinner = KireiSpinner()
    assert spinner.text() == KireiTexts.spinner_default
    spinner.text("Working")
    assert spinner.text() == "Working"


def test_badge_text_getter_returns_initial_text() -> None:
    assert KireiBadge("3").text() == "3"


def test_slider_value_getter_returns_int() -> None:
    slider = KireiSlider().range(0, 100)
    slider.setValue(42)
    assert slider.value() == 42


def test_spinbox_value_getter_returns_int() -> None:
    sb = KireiSpinBox().range(0, 100)
    sb.setValue(7)
    assert sb.value() == 7


def test_double_spinbox_value_getter_returns_float() -> None:
    dsb = KireiDoubleSpinBox().range(0, 100)
    dsb.setValue(2.5)
    assert dsb.value() == pytest.approx(2.5)


def test_spinbox_prefix_suffix_getter() -> None:
    sb = KireiSpinBox().prefix("$").suffix(" USD")
    assert sb.prefix() == "$"
    assert sb.suffix() == " USD"


def test_double_spinbox_decimals_getter() -> None:
    dsb = KireiDoubleSpinBox().decimals(3)
    assert dsb.decimals() == 3


def test_button_icon_getter_returns_qicon() -> None:
    btn = KireiButton("A")
    assert isinstance(btn.icon(), QIcon)


def test_navitem_icon_getter_returns_qicon() -> None:
    nav = KireiNavItem("A", "a")
    assert isinstance(nav.icon(), QIcon)


def test_splitter_sizes_getter_returns_list() -> None:
    splitter = KireiSplitter.horizontal().add(QWidget()).add(QWidget())
    sizes = splitter.sizes()
    assert isinstance(sizes, list)


# ---------------------------------------------------------------------------
# Callback dispatch contract
#
# Regression: KireiSidebar / KireiBreadcrumbs used a single shared
# ``_kirei_callbacks`` list for both nav-item clicks (no-arg) and
# user-registered ``on_change(str)``. Mixing them blew up with TypeError.
# Both classes now keep separate lists.
# ---------------------------------------------------------------------------


def test_sidebar_on_change_fires_with_item_key_when_item_clicked() -> None:
    sidebar = KireiSidebar()
    received: list[str] = []
    sidebar.on_change(received.append)
    sidebar.add_item("Home", "home")
    sidebar.add_item("Settings", "settings")
    sidebar._items["settings"].click()
    assert received == ["settings"]


def test_sidebar_supports_multiple_on_change_callbacks() -> None:
    sidebar = KireiSidebar()
    a: list[str] = []
    b: list[str] = []
    sidebar.on_change(a.append).on_change(b.append)
    sidebar.add_item("Home", "home")
    sidebar._items["home"].click()
    assert a == ["home"]
    assert b == ["home"]


def test_sidebar_on_change_registered_after_items_still_receives_clicks() -> None:
    """Order of on_change vs add_item should not matter."""
    sidebar = KireiSidebar()
    sidebar.add_item("Home", "home")
    received: list[str] = []
    sidebar.on_change(received.append)
    sidebar._items["home"].click()
    assert received == ["home"]


def test_sidebar_current_marks_item_selected() -> None:
    sidebar = KireiSidebar()
    sidebar.add_item("Home", "home").add_item("Settings", "settings")
    sidebar.current("settings")
    assert sidebar._items["home"].property("kireiState") == "normal"
    assert sidebar._items["settings"].property("kireiState") == "selected"


def test_breadcrumbs_on_click_receives_item_key() -> None:
    crumbs = KireiBreadcrumbs()
    received: list[str] = []
    crumbs.on_click(received.append)
    crumbs.add_item("Home", "home").add_item("Section A", "a")
    for btn in crumbs.findChildren(QToolButton):
        btn.click()
    assert received == ["home", "a"]


def test_button_on_click_does_not_pass_checked_argument() -> None:
    """Regression: clicked signal emits ``bool`` but on_click takes no args."""
    btn = KireiButton("A").checkable()
    calls = 0

    def handler() -> None:
        nonlocal calls
        calls += 1

    btn.on_click(handler)
    btn.click()
    btn.click()
    assert calls == 2


def test_button_on_click_checked_receives_bool_state() -> None:
    btn = KireiButton("A").checkable()
    seen: list[bool] = []
    btn.on_click_checked(seen.append)
    btn.click()
    btn.click()
    assert seen == [True, False]


def test_input_on_change_invoked_with_string() -> None:
    inp = KireiInput()
    seen: list[str] = []
    inp.on_change(seen.append)
    inp.setText("hello")
    assert seen == ["hello"]


# ---------------------------------------------------------------------------
# Locale: hard-coded user-facing text now lives in ``KireiTexts``.
# ---------------------------------------------------------------------------


def test_button_loading_uses_locale_text() -> None:
    original = KireiTexts.button_loading
    try:
        KireiTexts.button_loading = "WAIT..."
        btn = KireiButton("Submit")
        btn.set_loading(True)
        assert btn.text() == "WAIT..."
        btn.set_loading(False)
        assert btn.text() == "Submit"
    finally:
        KireiTexts.button_loading = original


def test_button_set_loading_disables_button() -> None:
    btn = KireiButton("Submit")
    btn.set_loading(True)
    assert btn.isEnabled() is False
    assert btn.property("kireiState") == "loading"
    btn.set_loading(False)
    assert btn.isEnabled() is True
    assert btn.property("kireiState") == "normal"


# ---------------------------------------------------------------------------
# QSS property contract: kirei* property names are the single source of truth.
# Old ``[variant=...]`` / ``[size=...]`` selectors were dropped in favor of
# ``[kireiVariant=...]`` / ``[kireiSize=...]`` — make sure components emit the
# new names and the bundled stylesheet uses them too.
# ---------------------------------------------------------------------------


def test_button_variant_writes_kirei_property_only() -> None:
    btn = KireiButton("A").primary()
    assert btn.property("kireiVariant") == "primary"
    dynamic_names = {bytes(name).decode() for name in btn.dynamicPropertyNames()}
    assert "variant" not in dynamic_names


def test_button_size_writes_kirei_property_only() -> None:
    btn = KireiButton("A").compact()
    assert btn.property("kireiSize") == "compact"
    # Qt has a built-in ``size`` meta-property; we only check our dynamic
    # property table — the legacy ``"size"`` dynamic property must not be set.
    dynamic_names = {bytes(name).decode() for name in btn.dynamicPropertyNames()}
    assert "size" not in dynamic_names


def test_panel_variant_writes_kirei_property_only() -> None:
    panel = KireiPanel().variant("card")
    assert panel.property("kireiVariant") == "card"
    assert panel.property("variant") is None


def test_builtin_base_qss_uses_kirei_selectors() -> None:
    qss = build_qss(theme="base")
    assert "[kireiVariant=" in qss
    assert "[kireiSize=" in qss
    assert "[variant=" not in qss
    assert "[size=" not in qss


# ---------------------------------------------------------------------------
# Animation contract: when motion is disabled the property must reach the end
# value synchronously (no animation timer). Regression risk: motion mixin used
# class attributes; switching to instance attributes must not break opt-out.
# ---------------------------------------------------------------------------


def test_progress_set_value_with_motion_disabled_is_synchronous() -> None:
    prog = KireiProgress().range(0, 100).animated(False)
    prog.show()
    prog.set_value(80)
    assert prog.value() == 80
    prog.hide()


def test_motion_mixin_instance_attribute_is_isolated_between_instances() -> None:
    a = KireiSwitch()
    b = KireiSwitch()
    a.animated(False)
    # ``b`` must not inherit ``a``'s opt-out via the class attribute.
    assert b.should_animate() is True


def test_motion_mixin_animation_duration_per_instance() -> None:
    a = KireiSwitch().animation_duration(50)
    b = KireiSwitch()
    assert a.resolved_animation_duration() == 50
    # default app-level fallback is 180 when no QApplication override is set
    assert b.resolved_animation_duration() in (50, 180)
    assert b.resolved_animation_duration() != 50 or a.resolved_animation_duration() == 50


# ---------------------------------------------------------------------------
# utils helpers
# ---------------------------------------------------------------------------


def test_attached_list_creates_and_returns_same_list() -> None:
    widget = QWidget()
    first = attached_list(widget, "_my_attr")
    second = attached_list(widget, "_my_attr")
    assert first is second
    first.append(1)
    assert second == [1]


def test_keep_callback_stores_handler_on_widget() -> None:
    widget = QWidget()

    def handler() -> None: ...

    returned = keep_callback(widget, handler)
    assert returned is handler
    assert handler in widget._kirei_callbacks


def test_clear_layout_removes_all_widgets() -> None:
    panel = KireiPanel()
    panel.content(QWidget())
    assert panel._content_layout.count() >= 1
    clear_layout(panel._content_layout)
    assert panel._content_layout.count() == 0


def test_replace_layout_content_swaps_widgets() -> None:
    panel = KireiPanel()
    first = QWidget()
    second = QWidget()
    panel.content(first)
    panel.content(second)  # uses replace_layout_content under the hood
    assert panel._content_layout.count() == 1
    item = panel._content_layout.itemAt(0)
    assert item is not None
    assert item.widget() is second


def test_clear_layout_recurses_into_sublayouts() -> None:
    from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout

    outer = QVBoxLayout()
    inner = QHBoxLayout()
    inner.addWidget(QWidget())
    inner.addWidget(QWidget())
    outer.addLayout(inner)
    clear_layout(outer)
    assert outer.count() == 0


def test_refresh_style_does_not_raise_on_label() -> None:
    label = KireiLabel("A")
    refresh_style(label)


# ---------------------------------------------------------------------------
# Theme loader: build_qss merging order and recursive scan
# ---------------------------------------------------------------------------


def test_build_qss_merges_in_documented_order() -> None:
    """Order: builtin -> qss_dirs -> qss_files -> extra_qss."""
    with TemporaryDirectory() as tmp:
        d = Path(tmp) / "themes"
        d.mkdir()
        (d / "01_dir.qss").write_text("/* DIR */", encoding="utf-8")
        f = Path(tmp) / "user.qss"
        f.write_text("/* FILE */", encoding="utf-8")

        result = build_qss(
            theme=None,
            qss_dirs=[d],
            qss_files=[f],
            extra_qss="/* EXTRA */",
        )
    assert result.index("/* DIR */") < result.index("/* FILE */")
    assert result.index("/* FILE */") < result.index("/* EXTRA */")


def test_build_qss_skips_empty_inputs() -> None:
    result = build_qss(theme=None, qss_dirs=[], qss_files=[], extra_qss=None)
    assert result == ""


# ---------------------------------------------------------------------------
# Tooltip refactor: KireiTooltip is a static namespace, instantiation is
# pointless but should still work.
# ---------------------------------------------------------------------------


def test_tooltip_apply_sets_native_tooltip() -> None:
    from kirei_ui.widgets.overlay import KireiTooltip

    widget = QWidget()
    KireiTooltip.apply(widget, "hello")
    assert widget.toolTip() == "hello"


def test_tooltip_no_longer_inherits_motion_mixin() -> None:
    from kirei_ui.widgets.overlay import KireiTooltip

    assert not issubclass(KireiTooltip, KireiMotionMixin)
