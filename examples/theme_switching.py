import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiText, KireiTitle  # noqa: E402
from kirei_ui.app import KireiApp, KireiWindow  # noqa: E402
from kirei_ui.inputs import KireiButton  # noqa: E402
from kirei_ui.layout import KireiCard, KireiHStack, KireiVStack  # noqa: E402


def main() -> int:
    theme_dir = ROOT / "styles" / "silicon_light"

    app = KireiApp()

    status = KireiText("Current theme: base")

    def use_builtin() -> None:
        app.set_theme(theme="base")
        status.text("Current theme: base")

    def use_silicon() -> None:
        app.set_theme(theme=None, qss_dirs=[theme_dir] if theme_dir.is_dir() else None)
        status.text("Current theme: styles/silicon_light")

    root = (
        KireiVStack()
        .padding(24)
        .spacing(12)
        .add(KireiTitle("Theme Switching Demo"))
        .add(status)
        .add(
            KireiCard()
            .title("Actions")
            .content(
                KireiHStack()
                .spacing(8)
                .add(KireiButton("Use Base Theme").on_click(use_builtin))
                .add(KireiButton("Use Silicon Theme").primary().on_click(use_silicon))
            )
        )
    )

    window = KireiWindow().title("KireiUI Theme Switching").size(880, 520).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
