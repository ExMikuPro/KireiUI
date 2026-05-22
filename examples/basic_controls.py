from pathlib import Path

from kirei_ui import KireiDivider, KireiText, KireiTitle
from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.inputs import (
    KireiButton,
    KireiCheckbox,
    KireiComboBox,
    KireiInput,
    KireiPassword,
    KireiRadio,
    KireiTextarea,
)
from kirei_ui.layout import KireiForm, KireiHStack, KireiVStack


def _resolve_theme_dirs() -> list[Path]:
    root = Path(__file__).resolve().parents[1]
    candidates = [
        root / "styles" / "silicon_light",
        root / "styles" / "aui_light",
        root / "styles" / "eui_light",
    ]
    for path in candidates:
        if path.is_dir():
            return [path]
    return []


def main() -> int:
    theme_dirs = _resolve_theme_dirs()
    app = KireiApp(
        qss_dirs=theme_dirs or None,
    )

    username = KireiInput().placeholder("Enter username").clearable()
    password = KireiPassword().placeholder("Enter password")
    bio = KireiTextarea().placeholder("Write something...")
    remember = KireiCheckbox("Remember me").checked()
    role = KireiComboBox().add_items(["User", "Admin", "Guest"]).current("User")

    root = (
        KireiVStack()
        .padding(32)
        .spacing(16)
        .add(KireiTitle("KireiUI Basic Controls"))
        .add(KireiText("This demo shows the basic KireiUI controls."))
        .add(KireiDivider())
        .add(
            KireiForm()
            .add_row("Username", username)
            .add_row("Password", password)
            .add_row("Bio", bio)
            .add_row("Remember", remember)
            .add_row("Role", role)
            .add_row("Option A", KireiRadio("Enabled").checked())
        )
        .add(
            KireiHStack()
            .stretch()
            .add(KireiButton("Cancel").subtle())
            .add(
                KireiButton("Submit")
                .primary()
                .on_click(lambda: print("submit", username.get_value(), role.get_value()))
            )
        )
    )

    window = KireiWindow().title("KireiUI Basic Controls").size(900, 600).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
