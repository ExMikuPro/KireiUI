import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kirei_ui import KireiText  # noqa: E402
from kirei_ui.app import KireiApp, KireiWindow  # noqa: E402
from kirei_ui.data import KireiPagination, KireiTable  # noqa: E402
from kirei_ui.inputs import KireiButton, KireiInput  # noqa: E402
from kirei_ui.layout import KireiCard, KireiForm, KireiHStack, KireiVStack  # noqa: E402
from kirei_ui.navigation import KireiSidebar, KireiTopBar  # noqa: E402


def _theme_dirs() -> list[Path]:
    theme = ROOT / "styles" / "silicon_light"
    return [theme] if theme.is_dir() else []


def main() -> int:
    app = KireiApp(qss_dirs=_theme_dirs() or None)

    sidebar = (
        KireiSidebar()
        .add_item("Overview", "overview")
        .add_item("Projects", "projects")
        .add_item("Settings", "settings")
        .current("overview")
    )

    table = (
        KireiTable()
        .columns(["Name", "Status", "Owner"])
        .rows([
            ["KireiUI", "Active", "Siling"],
            ["Desktop App", "Paused", "Miku"],
            ["Theme Pack", "Active", "Team"],
        ])
    )

    root = (
        KireiVStack()
        .padding(16)
        .spacing(12)
        .add(KireiTopBar("KireiUI Dashboard").trailing(KireiButton("New").primary()))
        .add(
            KireiHStack()
            .spacing(12)
            .add(sidebar)
            .add(
                KireiVStack()
                .spacing(12)
                .add(
                    KireiCard()
                    .title("Quick Filters")
                    .description("Simple dashboard filter form")
                    .content(
                        KireiForm()
                        .add_row("Keyword", KireiInput().placeholder("Search..."))
                        .add_row("Owner", KireiInput().placeholder("Owner"))
                    )
                )
                .add(KireiCard().title("Projects").content(table))
                .add(
                    KireiHStack()
                    .spacing(8)
                    .add(KireiText("Use pagination to navigate data."))
                    .add(KireiPagination().total(128).page_size(10).page(1))
                )
            )
        )
    )

    window = KireiWindow().title("KireiUI Dashboard").size(1200, 820).content(root)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
