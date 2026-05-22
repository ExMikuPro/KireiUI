from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget

from kirei_ui.app.application import KireiApp
from kirei_ui.app.window import KireiWindow
from kirei_ui.widgets.button import KireiButton
from kirei_ui.widgets.choice import KireiCheckbox, KireiRadio
from kirei_ui.widgets.data_display import (
    KireiFilterBar,
    KireiList,
    KireiPagination,
    KireiSearchBox,
    KireiTable,
    KireiTree,
)
from kirei_ui.widgets.datetime import KireiDateEdit, KireiDateTimeEdit, KireiTimeEdit
from kirei_ui.widgets.desktop import (
    KireiAction,
    KireiColorDialog,
    KireiFileDialog,
    KireiMenuBar,
    KireiShortcut,
    KireiStatusBar,
    KireiSystemTray,
)
from kirei_ui.widgets.divider import KireiDivider
from kirei_ui.widgets.feedback import (
    KireiAlert,
    KireiBadge,
    KireiEmpty,
    KireiProgress,
    KireiSpinner,
    KireiTag,
)
from kirei_ui.widgets.input import KireiInput, KireiPassword, KireiTextarea
from kirei_ui.widgets.label import KireiLabel, KireiText, KireiTitle
from kirei_ui.widgets.layout_plus import (
    KireiActionGroup,
    KireiBreadcrumbs,
    KireiCard,
    KireiMenu,
    KireiNavItem,
    KireiSection,
    KireiSidebar,
    KireiToolbar,
    KireiTopBar,
)
from kirei_ui.widgets.number import KireiDoubleSpinBox, KireiSlider, KireiSpinBox
from kirei_ui.widgets.overlay import (
    KireiConfirm,
    KireiDialog,
    KireiDrawer,
    KireiMessageBox,
    KireiPopover,
    KireiTooltip,
)
from kirei_ui.widgets.select import KireiComboBox
from kirei_ui.widgets.switch import KireiSwitch


@pytest.fixture(scope="module", autouse=True)
def _app() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_window_title_returns_self() -> None:
    window = KireiWindow()
    assert window.title("Demo") is window


def test_window_size_with_args_returns_self() -> None:
    window = KireiWindow()
    assert window.size(900, 600) is window


def test_window_size_no_args_returns_qsize() -> None:
    window = KireiWindow()
    assert isinstance(window.size(), QSize)


def test_window_content_returns_self() -> None:
    window = KireiWindow()
    assert window.content(QWidget()) is window


def test_window_set_content_old_api_still_works() -> None:
    window = KireiWindow()
    widget = QWidget()
    window.set_content(widget)
    assert window.centralWidget() is widget


def test_button_primary_compact_returns_self() -> None:
    button = KireiButton("A")
    assert button.primary().compact() is button


def test_button_on_click_returns_self() -> None:
    button = KireiButton("A")

    def callback() -> None:
        return None

    assert button.on_click(callback) is button


def test_button_on_click_invoked_once_by_click() -> None:
    QApplication.instance() or QApplication([])
    button = KireiButton("A")
    calls = {"count": 0}

    def callback() -> None:
        calls["count"] += 1

    button.on_click(callback)
    button.click()
    assert calls["count"] == 1


def test_button_on_click_ignores_checked_argument() -> None:
    QApplication.instance() or QApplication([])
    button = KireiButton("A").checkable()
    calls = {"count": 0}

    def callback() -> None:
        calls["count"] += 1

    button.on_click(callback)
    button.click()
    assert calls["count"] == 1


def test_button_checkable_on_click_checked_receives_bool() -> None:
    QApplication.instance() or QApplication([])
    values: list[bool] = []
    button = KireiButton("A").checkable().on_click_checked(lambda checked: values.append(checked))

    button.click()
    button.click()
    assert values == [True, False]


def test_button_chain_with_callback_stays_chainable() -> None:
    button = KireiButton("A")
    chained = button.primary().on_click(lambda: None).compact()
    assert chained is button


def test_qt_native_clicked_connect_still_works() -> None:
    QApplication.instance() or QApplication([])
    button = KireiButton("A")
    calls = {"count": 0}

    def callback() -> None:
        calls["count"] += 1

    button.clicked.connect(callback)
    button.click()
    assert calls["count"] == 1


def test_button_text_getter_and_setter_chain() -> None:
    button = KireiButton("A")
    assert button.text() == "A"
    assert button.text("B") is button
    assert button.text() == "B"


def test_app_load_qss_returns_self() -> None:
    with TemporaryDirectory() as tmp:
        qss_file = Path(tmp) / "app.qss"
        qss_file.write_text("QLabel { color: #123; }", encoding="utf-8")

        class _FakeApp:
            def __init__(self) -> None:
                self._style = ""

            def styleSheet(self) -> str:
                return self._style

            def setStyleSheet(self, value: str) -> None:
                self._style = value

        app = _FakeApp()
        assert KireiApp.load_qss(app, qss_file) is app


def test_app_set_theme_returns_self() -> None:
    class _FakeApp:
        def __init__(self) -> None:
            self._style = ""

        def setStyleSheet(self, value: str) -> None:
            self._style = value

        def set_theme(
            self,
            theme: str | None = "base",
            qss_files: list[str | Path] | None = None,
            extra_qss: str | None = None,
        ) -> _FakeApp:
            return KireiApp.set_theme(self, theme=theme, qss_files=qss_files, extra_qss=extra_qss)

    app = _FakeApp()
    assert KireiApp.set_theme(app, theme="base") is app
    assert KireiApp.theme(app, "base") is app


def test_label_text_returns_self() -> None:
    label = KireiLabel()
    assert label.text("A") is label


def test_input_placeholder_returns_self() -> None:
    control = KireiInput()
    assert control.placeholder("A") is control


def test_title_and_text_role_defaults() -> None:
    assert KireiTitle("A").property("kireiRole") == "title"
    assert KireiText("A").property("kireiRole") == "text"


def test_input_value_and_get_value() -> None:
    control = KireiInput()
    assert control.value("A").get_value() == "A"


def test_password_default_echo_mode_is_password() -> None:
    control = KireiPassword()
    assert control.echoMode() == control.EchoMode.Password


def test_checkbox_checked_and_is_checked() -> None:
    control = KireiCheckbox()
    assert control.checked().is_checked() is True


def test_radio_checked_and_is_checked() -> None:
    control = KireiRadio("A")
    assert control.checked().is_checked() is True


def test_textarea_value_and_get_value() -> None:
    control = KireiTextarea()
    assert control.value("A").get_value() == "A"


def test_combobox_add_items_current_and_get_value() -> None:
    control = KireiComboBox()
    assert control.add_items(["A", "B"]).current("B").get_value() == "B"


def test_input_on_change_returns_self() -> None:
    control = KireiInput()
    assert control.on_change(lambda _value: None) is control


def test_input_on_submit_returns_self() -> None:
    control = KireiInput()
    assert control.on_submit(lambda: None) is control


def test_divider_default_role() -> None:
    divider = KireiDivider()
    assert divider.property("kireiRole") == "divider"


def test_button_on_click_returns_self_again() -> None:
    button = KireiButton("A")
    assert button.on_click(lambda: None) is button


def test_switch_checked_and_is_checked() -> None:
    control = KireiSwitch("A")
    assert control.checked().is_checked() is True


def test_slider_range_value_get_value() -> None:
    control = KireiSlider()
    assert control.range(0, 100).value(50).get_value() == 50


def test_spinbox_range_value_get_value() -> None:
    control = KireiSpinBox()
    assert control.range(0, 10).value(3).get_value() == 3


def test_double_spinbox_value_get_value() -> None:
    control = KireiDoubleSpinBox()
    assert control.value(1.5).get_value() == pytest.approx(1.5)


def test_alert_success_variant() -> None:
    control = KireiAlert()
    assert control.success().property("kireiVariant") == "success"


def test_badge_warning_variant() -> None:
    control = KireiBadge("A")
    assert control.warning().property("kireiVariant") == "warning"


def test_tag_danger_variant() -> None:
    control = KireiTag("A")
    assert control.danger().property("kireiVariant") == "danger"


def test_progress_value_get_value() -> None:
    control = KireiProgress()
    assert control.value(50).get_value() == 50


def test_empty_title_returns_self() -> None:
    control = KireiEmpty()
    assert control.title("No data") is control


def test_datetime_chainable_methods_return_self() -> None:
    date = KireiDateEdit()
    time = KireiTimeEdit()
    dt = KireiDateTimeEdit()
    assert date.display_format("yyyy-MM-dd").calendar_popup() is date
    assert time.display_format("HH:mm:ss") is time
    assert dt.display_format("yyyy-MM-dd HH:mm:ss").calendar_popup() is dt


def test_feedback_chainable_methods_return_self() -> None:
    alert = KireiAlert()
    tag = KireiTag("A")
    progress = KireiProgress()
    spinner = KireiSpinner()
    assert alert.closable().on_close(lambda: None) is alert
    assert tag.closable().on_close(lambda: None) is tag
    assert progress.text_visible().indeterminate() is progress
    assert spinner.running(False).size("small") is spinner


def test_card_and_section_chainable() -> None:
    card = KireiCard()
    section = KireiSection()
    assert (
        card.title("A").description("B").content(QWidget()).footer(QWidget()).variant("x") is card
    )
    assert section.title("A").description("B").content(QWidget()).actions(QWidget()) is section


def test_topbar_sidebar_toolbar_chainable() -> None:
    topbar = KireiTopBar()
    sidebar = KireiSidebar()
    toolbar = KireiToolbar()
    assert topbar.title("A").leading(QWidget()).trailing(QWidget()).content(QWidget()) is topbar
    assert (
        sidebar.add_item("A", "a").add_widget(QWidget()).current("a").on_change(lambda _k: None)
        is sidebar
    )
    assert toolbar.add(QWidget()).separator().stretch() is toolbar


def test_nav_breadcrumb_actiongroup_menu_chainable() -> None:
    nav = KireiNavItem("A", "a")
    crumbs = KireiBreadcrumbs()
    group = KireiActionGroup()
    menu = KireiMenu()
    anchor = QWidget()
    anchor.resize(10, 10)
    assert nav.text("B").key("b").selected().on_click(lambda: None) is nav
    assert crumbs.add_item("Home", "home").on_click(lambda _k: None) is crumbs
    assert group.add(QWidget()).spacing(6) is group
    assert menu.add_action("A").add_separator() is menu


def test_overlay_components_chainable_and_variants() -> None:
    dialog = KireiDialog()
    confirm = KireiConfirm()
    msg = KireiMessageBox()
    drawer = KireiDrawer()
    pop = KireiPopover()
    w = QWidget()
    result = dialog.title("A").content(QWidget()).footer(QWidget()).modal().open().close_dialog()
    assert result is dialog
    assert (
        confirm.title("A")
        .description("B")
        .confirm_text("OK")
        .cancel_text("No")
        .on_confirm(lambda: None)
        .on_cancel(lambda: None)
        .open()
        is confirm
    )
    assert msg.title("A").text("B").warning().danger().info().open() is msg
    assert drawer.title("A").content(QWidget()).side("left").open().close_drawer() is drawer
    assert pop.content(QWidget()) is pop
    assert KireiTooltip.apply(w, "tip") is w


def test_table_and_list_and_tree_chainable() -> None:
    table = KireiTable().columns(["A", "B"]).add_row([1, 2]).rows([[3, 4]])
    assert table.selected_row() >= -1
    assert table.clear_rows() is table

    lst = KireiList().add_item("A").add_items(["B", "C"]).current("B")
    assert lst.get_value() == "B"

    tree = KireiTree().headers(["Name"]).add_item(["x"])
    assert tree.clear_items() is tree


def test_search_filter_pagination_chainable() -> None:
    search = KireiSearchBox().placeholder("Search").value("A")
    assert search.get_value() == "A"
    assert search.on_search(lambda _v: None).on_change(lambda _v: None) is search

    bar = KireiFilterBar().add_filter(QWidget()).add_action(QWidget())
    assert bar.clear_filters() is bar

    pages = KireiPagination().total(100).page_size(10).page(2)
    assert pages.on_change(lambda _p: None) is pages


def test_desktop_helpers_chainable() -> None:
    action = KireiAction("Open").text("Open").shortcut("Ctrl+O").tooltip("Open file")
    assert action.enabled().disabled(False).on_trigger(lambda: None) is action
    assert action.qt_action() is not None

    w = QWidget()
    shortcut = KireiShortcut("Ctrl+K", w)
    assert shortcut.on_trigger(lambda: None).enabled() is shortcut

    menubar = KireiMenuBar()
    menubar.add_menu("File")
    assert menubar.add_action_to("File", action) is menubar

    status = KireiStatusBar()
    assert status.message("Ready", 10).clear().add(QWidget()) is status


def test_system_tray_and_dialog_tools_exist() -> None:
    tray = KireiSystemTray()
    assert tray.tooltip("Tray").show_tray().hide_tray().on_activate(lambda _r: None) is tray

    assert callable(KireiFileDialog.open_file)
    assert callable(KireiFileDialog.save_file)
    assert callable(KireiFileDialog.open_directory)
    assert callable(KireiColorDialog.get_color)
