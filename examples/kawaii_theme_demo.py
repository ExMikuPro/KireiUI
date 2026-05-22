from pathlib import Path

from PySide6.QtWidgets import QLabel

from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.data import KireiList
from kirei_ui.feedback import KireiAlert, KireiBadge, KireiProgress, KireiTag
from kirei_ui.inputs import KireiButton, KireiCheckbox, KireiComboBox, KireiInput
from kirei_ui.layout import KireiCard, KireiHStack, KireiPanel, KireiVStack
from kirei_ui.navigation import KireiSidebar, KireiTabs, KireiTopBar


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    app = KireiApp(
        qss_dirs=[project_root / "styles" / "silicon_light"],
    )

    normal_input = KireiInput().placeholder("Normal input")
    error_input = KireiInput().placeholder("Error input")
    error_input.setProperty("kireiState", "error")
    disabled_input = KireiInput().placeholder("Disabled input").disabled()

    sidebar = (
        KireiSidebar()
        .add_item("Dashboard", "dashboard")
        .add_item("Settings", "settings")
        .current("dashboard")
    )

    tabs = KireiTabs().add_tab("Overview", QLabel("Overview content")).add_tab(
        "Reports", QLabel("Reports content")
    )

    demo_list = KireiList().add_items(["Alpha", "Beta", "Gamma"]).current("Beta")

    root = (
        KireiVStack()
        .padding(20)
        .spacing(14)
        .add(KireiTopBar("Silicon Light Theme Demo"))
        .add(
            KireiHStack()
            .spacing(12)
            .add(KireiButton("Primary").primary())
            .add(KireiButton("Secondary").variant("secondary"))
            .add(KireiButton("Danger").danger())
            .add(KireiButton("Ghost").variant("ghost"))
        )
        .add(
            KireiHStack()
            .spacing(12)
            .add(KireiButton("Small").sized("sm"))
            .add(KireiButton("Medium").sized("md"))
            .add(KireiButton("Large").sized("lg"))
        )
        .add(
            KireiCard()
            .title("Inputs")
            .description("normal / disabled / error")
            .content(
                KireiVStack()
                .spacing(8)
                .add(normal_input)
                .add(error_input)
                .add(disabled_input)
                .add(KireiCheckbox("Remember me").checked())
                .add(KireiComboBox().add_items(["User", "Admin", "Guest"]).current("User"))
            )
        )
        .add(
            KireiHStack()
            .spacing(8)
            .add(KireiAlert("Info", "Information").info())
            .add(KireiAlert("Success", "Saved").success())
            .add(KireiAlert("Warning", "Check fields").warning())
            .add(KireiAlert("Danger", "Operation failed").danger())
        )
        .add(
            KireiHStack()
            .spacing(8)
            .add(KireiBadge("Beta").primary())
            .add(KireiTag("Stable").success())
            .add(KireiTag("Deprecated").warning())
        )
        .add(KireiProgress().range(0, 100).value(65).text_visible())
        .add(KireiPanel().content(sidebar))
        .add(tabs)
        .add(KireiCard().title("List").content(demo_list))
    )

    window = KireiWindow().title("KireiUI Silicon Theme Demo").size(1120, 820).content(root)
    window.show()

    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
