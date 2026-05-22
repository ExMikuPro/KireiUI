from PySide6.QtWidgets import QLabel, QLineEdit

from kirei_ui import (
    KireiApp,
    KireiButton,
    KireiForm,
    KireiGrid,
    KireiHStack,
    KireiVStack,
    KireiWindow,
)


def main() -> int:
    app = KireiApp()

    def on_primary_clicked() -> None:
        print("Primary clicked")

    def on_toggle_clicked(checked: bool) -> None:
        print(f"Toggle checked: {checked}")

    root = (
        KireiVStack()
        .padding(32)
        .spacing(16)
        .add(
            KireiHStack()
            .spacing(8)
            .add(KireiButton("Default"))
            .add(KireiButton("Primary").primary().on_click(on_primary_clicked))
            .add(KireiButton("Link").link())
            .add(KireiButton("Subtle").subtle())
            .add(KireiButton("Danger").danger())
            .add(KireiButton("Warning").warning())
            .add(KireiButton("Toggle").checkable().on_click_checked(on_toggle_clicked))
            .stretch()
        )
        .add(
            KireiHStack()
            .spacing(8)
            .add(KireiButton("Compact").compact())
            .add(KireiButton("Compact Primary").primary().compact())
            .stretch()
        )
        .add(
            KireiGrid()
            .spacing(8)
            .add_at(QLabel("Grid A"), 0, 0)
            .add_at(QLabel("Grid B"), 0, 1)
            .add_at(QLabel("Grid C"), 1, 0, 1, 2)
        )
        .add(
            KireiForm()
            .spacing(8)
            .add_row("Name", QLineEdit())
            .add_row("Email", QLineEdit())
        )
        .stretch()
    )

    window = KireiWindow().title("KireiUI AUI Button Test").size(900, 600).content(root)
    window.show()

    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
