import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiText, KireiTitle  # noqa: E402
from kirei_ui.app import KireiApp, KireiWindow  # noqa: E402
from kirei_ui.inputs import KireiButton, KireiInput  # noqa: E402
from kirei_ui.layout import KireiCard, KireiVStack  # noqa: E402


def main() -> int:
    style_file = ROOT / "styles" / "silicon_light" / "99_overrides.qss"

    app = KireiApp(
        theme="base",
        qss_files=[style_file] if style_file.is_file() else None,
        extra_qss='QPushButton[kirei="button"] { min-height: 36px; }',
    )

    root = (
        KireiVStack()
        .padding(20)
        .spacing(12)
        .add(KireiTitle("QSS Custom Theme Demo"))
        .add(KireiText("This demo combines base theme + local qss file + extra_qss."))
        .add(
            KireiCard()
            .title("Form")
            .content(
                KireiVStack()
                .spacing(8)
                .add(KireiInput().placeholder("Your name"))
                .add(KireiButton("Submit").primary())
            )
        )
    )

    window = KireiWindow().title("KireiUI QSS Theme").size(920, 580).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
