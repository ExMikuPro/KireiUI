import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiTitle  # noqa: E402
from kirei_ui.app import KireiApp, KireiWindow  # noqa: E402
from kirei_ui.inputs import KireiButton  # noqa: E402
from kirei_ui.layout import KireiVStack  # noqa: E402


def _theme_dirs() -> list[Path]:
    theme = ROOT / "styles" / "silicon_light"
    return [theme] if theme.is_dir() else []


def main() -> int:
    app = KireiApp(qss_dirs=_theme_dirs() or None)

    root = (
        KireiVStack()
        .padding(24)
        .spacing(12)
        .add(KireiTitle("Hello KireiUI"))
        .add(KireiButton("Click Me").primary().on_click(lambda: print("clicked")))
    )

    window = KireiWindow().title("KireiUI Hello").size(720, 420).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
