from PySide6.QtCore import QDate, QDateTime, QTime

from kirei_ui import KireiMenu, KireiTitle
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.data import KireiSearchBox
from kirei_ui.desktop import KireiMenuBar, KireiStatusBar, KireiSystemTray
from kirei_ui.feedback import (
    KireiAlert,
    KireiBadge,
    KireiEmpty,
    KireiProgress,
    KireiSpinner,
    KireiTag,
)
from kirei_ui.inputs import (
    KireiButton,
    KireiDateEdit,
    KireiDateTimeEdit,
    KireiDoubleSpinBox,
    KireiInput,
    KireiSlider,
    KireiSpinBox,
    KireiSwitch,
    KireiTimeEdit,
)
from kirei_ui.layout import (
    KireiActionGroup,
    KireiCard,
    KireiForm,
    KireiHStack,
    KireiSection,
    KireiToolbar,
    KireiVStack,
)
from kirei_ui.navigation import KireiBreadcrumbs, KireiSidebar, KireiTopBar
from kirei_ui.overlay import (
    KireiConfirm,
    KireiDialog,
    KireiDrawer,
    KireiMessageBox,
    KireiPopover,
    KireiTooltip,
)


def main() -> int:
    app = KireiApp()
    _ = (KireiMenuBar, KireiStatusBar, KireiSystemTray, KireiSearchBox)

    menu_anchor = KireiButton("Open Menu")
    menu = (
        KireiMenu()
        .add_action("Refresh", lambda: print("refresh"))
        .add_separator()
        .add_action("Delete")
    )
    menu_anchor.on_click(lambda: menu.popup_at(menu_anchor))

    popover_anchor = KireiButton("Open Popover")
    popover = KireiPopover().content(
        KireiVStack().add(KireiTitle("Popover")).add(KireiInput("hello"))
    )
    popover_anchor.on_click(lambda: popover.popup_at(popover_anchor))

    dialog = KireiDialog().title("Dialog").content(KireiInput("Dialog content"))
    confirm = KireiConfirm().title("Confirm").description("Are you sure?")
    drawer = KireiDrawer().title("Drawer").content(KireiInput("Drawer content"))
    msg = KireiMessageBox().title("Message").text("Info message").info()

    sidebar = (
        KireiSidebar()
        .add_item("Overview", "overview")
        .add_item("Settings", "settings")
        .current("overview")
    )

    root = (
        KireiVStack()
        .padding(24)
        .spacing(12)
        .add(KireiTopBar("KireiUI Component Gallery").trailing(KireiButton("Top Action")))
        .add(KireiBreadcrumbs().add_item("Home", "home").add_item("Gallery", "gallery"))
        .add(KireiToolbar().add(KireiButton("New")).separator().add(KireiButton("Edit")).stretch().add(menu_anchor))
        .add(sidebar)
        .add(
            KireiCard().title("Card").description("Simple card").content(KireiInput("card body"))
        )
        .add(
            KireiSection()
            .title("Section")
            .description("Section description")
            .content(KireiInput("content"))
        )
        .add(
            KireiForm()
            .add_row("Switch", KireiSwitch("Enable notifications").checked())
            .add_row("Slider", KireiSlider().range(0, 100).value(35))
            .add_row("Spin", KireiSpinBox().range(0, 10).value(3))
            .add_row("Double", KireiDoubleSpinBox().range(0.0, 10.0).value(1.5))
            .add_row("Date", KireiDateEdit().value(QDate.currentDate()).calendar_popup())
            .add_row("Time", KireiTimeEdit().value(QTime.currentTime()))
            .add_row(
                "DateTime",
                KireiDateTimeEdit().value(QDateTime.currentDateTime()).calendar_popup(),
            )
        )
        .add(KireiAlert("Info", "Everything works").info())
        .add(KireiHStack().spacing(8).add(KireiBadge("Default")).add(KireiTag("Danger").danger()))
        .add(KireiProgress().range(0, 100).value(60).text_visible())
        .add(KireiSpinner("Loading...").start())
        .add(
            KireiEmpty("No Data", "Try changing your filters.").action(
                KireiButton("Refresh").primary()
            )
        )
        .add(
            KireiActionGroup()
            .spacing(8)
            .add(KireiButton("Dialog").on_click(lambda: dialog.open()))
            .add(KireiButton("Confirm").on_click(lambda: confirm.open()))
            .add(KireiButton("Drawer").on_click(lambda: drawer.open()))
            .add(KireiButton("Message").on_click(lambda: msg.open()))
            .add(popover_anchor)
        )
    )

    KireiTooltip.apply(menu_anchor, "Click to open popup menu")

    window = KireiWindow().title("KireiUI Component Gallery").size(1080, 960).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
