"""KireiUI Gallery — 仿 PyQt-SiliconUI 的示例总览程序.

布局: 左侧 KireiSidebar 切换分类, 右侧 KireiStack 切换页面.
每页用 KireiSection + KireiCard 把同类控件分组展示.
"""

from __future__ import annotations

from kirei_ui import (
    KireiAlert,
    KireiApp,
    KireiBadge,
    KireiButton,
    KireiCard,
    KireiCheckbox,
    KireiComboBox,
    KireiConfirm,
    KireiDateEdit,
    KireiDivider,
    KireiDrawer,
    KireiEmpty,
    KireiForm,
    KireiHStack,
    KireiIconButton,
    KireiInput,
    KireiList,
    KireiMessageBox,
    KireiPassword,
    KireiProgress,
    KireiRadio,
    KireiScroll,
    KireiSection,
    KireiSidebar,
    KireiSlider,
    KireiSpinBox,
    KireiSpinner,
    KireiStack,
    KireiSwitch,
    KireiTable,
    KireiTabs,
    KireiTag,
    KireiText,
    KireiTextarea,
    KireiTitle,
    KireiTopBar,
    KireiVStack,
    KireiWindow,
)

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------


def _section(title: str, description: str, body) -> KireiSection:
    return KireiSection().title(title).description(description).content(body)


def _card(title: str, description: str, body) -> KireiCard:
    return KireiCard().title(title).description(description).content(body)


def build_home_page() -> KireiVStack:
    hero = (
        KireiVStack()
        .spacing(8)
        .add(KireiTitle("KireiUI Gallery"))
        .add(
            KireiText(
                "A fluent, chainable component kit on top of PySide6. "
                "Browse the categories on the left to explore widgets, "
                "containers and feedback patterns."
            ).word_wrap()
        )
    )

    cards = (
        KireiHStack()
        .spacing(16)
        .add(
            _card(
                "Widgets",
                "Buttons, inputs, toggles and the rest of the daily-driver controls.",
                KireiBadge("12+ controls").primary(),
            ),
            stretch=1,
        )
        .add(
            _card(
                "Containers",
                "Stacks, grids, cards and tabs to compose your screens.",
                KireiBadge("Layouts").success(),
            ),
            stretch=1,
        )
        .add(
            _card(
                "Feedback",
                "Alerts, dialogs, drawers and progress for user-facing messaging.",
                KireiBadge("Overlays").warning(),
            ),
            stretch=1,
        )
    )

    quick_actions = (
        KireiHStack()
        .spacing(8)
        .add(KireiButton("Get started").primary())
        .add(KireiButton("Read docs").subtle())
        .add(KireiButton("Source").link())
    )

    return (
        KireiVStack()
        .padding(24)
        .spacing(24)
        .add(hero)
        .add(KireiDivider())
        .add(cards)
        .add(quick_actions)
        .stretch()
    )


def build_widgets_page() -> KireiVStack:
    buttons = (
        KireiHStack()
        .spacing(8)
        .add(KireiButton("Default"))
        .add(KireiButton("Primary").primary())
        .add(KireiButton("Subtle").subtle())
        .add(KireiButton("Link").link())
        .add(KireiButton("Warning").warning())
        .add(KireiButton("Danger").danger())
        .stretch()
    )

    inputs = (
        KireiForm()
        .spacing(12)
        .add_row("Username", KireiInput().placeholder("Enter username").clearable())
        .add_row("Password", KireiPassword().placeholder("Enter password"))
        .add_row("Bio", KireiTextarea().placeholder("Write something..."))
    )

    choices = (
        KireiHStack()
        .spacing(16)
        .add(KireiCheckbox("Remember me").checked())
        .add(KireiRadio("Active").checked())
        .add(KireiRadio("Paused"))
        .add(KireiSwitch("Notifications").checked())
        .stretch()
    )

    pickers = (
        KireiForm()
        .spacing(12)
        .add_row("Role", KireiComboBox().add_items(["User", "Admin", "Guest"]).current("User"))
        .add_row("Date", KireiDateEdit().calendar_popup())
        .add_row("Volume", KireiSlider().range(0, 100).value(40))
        .add_row("Quantity", KireiSpinBox().range(0, 99).value(3))
    )

    tags = (
        KireiHStack()
        .spacing(8)
        .add(KireiTag("default").default())
        .add(KireiTag("primary").primary())
        .add(KireiTag("success").success())
        .add(KireiTag("warning").warning())
        .add(KireiTag("danger").danger())
        .stretch()
    )

    icon_buttons = (
        KireiHStack()
        .spacing(8)
        .add(KireiIconButton("settings").tooltip("Settings"))
        .add(KireiIconButton("save").primary().tooltip("Save"))
        .add(KireiIconButton("search").subtle().tooltip("Search"))
        .add(KireiIconButton("delete").danger().tooltip("Delete"))
        .add(KireiIconButton("warning").warning().tooltip("Warn"))
        .add(KireiIconButton("heart").circle().primary().tooltip("Like"))
        .add(KireiIconButton("plus").large().circle().primary().tooltip("Add"))
        .stretch()
    )

    return (
        KireiVStack()
        .padding(24)
        .spacing(24)
        .add(_section("Buttons", "Six semantic variants share the same chainable API.", buttons))
        .add(_section("Inputs", "Single-line, password and multi-line text entry.", inputs))
        .add(_section("Choices", "Boolean and exclusive selection controls.", choices))
        .add(_section("Pickers", "Combo boxes, dates, sliders and spin boxes.", pickers))
        .add(_section("Tags", "Compact pills for status and categorization.", tags))
        .add(
            _section(
                "Icon buttons",
                "Square or circular controls that show only an icon.",
                icon_buttons,
            )
        )
        .stretch()
    )


def build_containers_page() -> KireiVStack:
    cards_demo = (
        KireiHStack()
        .spacing(16)
        .add(
            _card(
                "Self-contained block",
                "Cards bundle a title, description, content and footer slot.",
                KireiText("Replace this slot with any widget.").word_wrap(),
            ),
            stretch=1,
        )
        .add(
            _card(
                "Bordered surface",
                "Use cards to group related options or stats.",
                KireiBadge("New").primary(),
            ),
            stretch=1,
        )
    )

    tabs = (
        KireiTabs()
        .add_tab("Overview", KireiVStack().padding(16).add(KireiText("Overview pane")))
        .add_tab("Details", KireiVStack().padding(16).add(KireiText("Details pane")))
        .add_tab("History", KireiVStack().padding(16).add(KireiText("History pane")))
    )

    table = (
        KireiTable()
        .columns(["Name", "Status", "Owner"])
        .rows(
            [
                ["Auth migration", "in-progress", "alice"],
                ["Theme refresh", "review", "bob"],
                ["Docs overhaul", "done", "carol"],
            ]
        )
    )

    listing = (
        KireiList().add_items(["Mercury", "Venus", "Earth", "Mars", "Jupiter"]).current("Earth")
    )

    return (
        KireiVStack()
        .padding(24)
        .spacing(24)
        .add(_section("Cards", "Bordered surfaces for grouping related content.", cards_demo))
        .add(_section("Tabs", "Switch between sibling views without losing context.", tabs))
        .add(_section("Table", "Tabular data with simple, fluent setup.", table))
        .add(_section("List", "Vertical selectable items with single-selection.", listing))
        .stretch()
    )


def _build_dialog_actions(window: KireiWindow) -> KireiHStack:
    confirm = (
        KireiConfirm(window).title("Delete record?").description("This action cannot be undone.")
    )
    info = KireiMessageBox(window).title("Heads up").text("All changes have been saved.").info()
    danger = KireiMessageBox(window).title("Failure").text("Could not reach the server.").danger()
    drawer = (
        KireiDrawer(window)
        .title("Filters")
        .content(
            KireiVStack()
            .spacing(8)
            .add(KireiCheckbox("Open"))
            .add(KireiCheckbox("In review"))
            .add(KireiCheckbox("Done").checked())
        )
        .side("right")
    )

    return (
        KireiHStack()
        .spacing(8)
        .add(KireiButton("Confirm").primary().on_click(lambda: confirm.open()))
        .add(KireiButton("Info").on_click(lambda: info.open()))
        .add(KireiButton("Danger").danger().on_click(lambda: danger.open()))
        .add(KireiButton("Open drawer").subtle().on_click(lambda: drawer.toggle()))
        .stretch()
    )


def build_feedback_page(window: KireiWindow) -> KireiVStack:
    alerts = (
        KireiVStack()
        .spacing(8)
        .add(KireiAlert("Info", "Heads-up alert with neutral tone.").info())
        .add(KireiAlert("Success", "The build pipeline finished cleanly.").success())
        .add(KireiAlert("Warning", "Token will expire in 30 minutes.").warning())
        .add(KireiAlert("Danger", "Connection to the server was lost.").danger())
    )

    progress = (
        KireiVStack()
        .spacing(8)
        .add(KireiProgress().range(0, 100).value(35))
        .add(KireiProgress().range(0, 100).value(72).success())
        .add(KireiProgress().indeterminate())
    )

    spinners = (
        KireiHStack()
        .spacing(16)
        .add(KireiSpinner("Loading..."))
        .add(KireiSpinner("Refreshing"))
        .stretch()
    )

    empty = KireiEmpty("No results", "Try adjusting your filters or search keywords.").action(
        KireiButton("Reset filters").primary()
    )

    return (
        KireiVStack()
        .padding(24)
        .spacing(24)
        .add(_section("Alerts", "Inline banners with semantic variants.", alerts))
        .add(
            _section(
                "Dialogs",
                "Modal confirmation, info, danger and drawer.",
                _build_dialog_actions(window),
            )
        )
        .add(_section("Progress", "Determinate, success and indeterminate variants.", progress))
        .add(_section("Spinners", "Loading indicators for async work.", spinners))
        .add(_section("Empty state", "Friendly placeholder when there is nothing to show.", empty))
        .stretch()
    )


def build_about_page() -> KireiVStack:
    body = (
        KireiVStack()
        .spacing(12)
        .add(KireiTitle("About KireiUI"))
        .add(
            KireiText(
                "KireiUI is a fluent component kit on top of PySide6. Each widget exposes "
                "a chainable API so screens can be built top-down in pure Python, "
                "while QSS handles the visual layer."
            ).word_wrap()
        )
        .add(KireiDivider())
        .add(
            KireiHStack()
            .spacing(8)
            .add(KireiBadge("PySide6").primary())
            .add(KireiBadge("Fluent API").success())
            .add(KireiBadge("Theming via QSS").neutral())
        )
    )

    return KireiVStack().padding(24).add(body).stretch()


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------


def _wrap_in_scroll(page) -> KireiScroll:
    return KireiScroll().resizable().content(page)


def _build_icon_sidebar(pages: KireiStack) -> KireiSidebar:
    entries = [
        ("home", "home", "Home"),
        ("widgets", "grid", "Widgets"),
        ("containers", "board", "Containers"),
        ("feedback", "alert", "Feedback"),
        ("about", "info", "About"),
    ]

    sidebar = KireiSidebar()
    sidebar.setFixedWidth(72)
    buttons: dict[str, KireiIconButton] = {}

    def select(key: str) -> None:
        for k, btn in buttons.items():
            btn.checked(k == key)
        pages.current(key)

    for key, icon_name, tip in entries:
        button = (
            KireiIconButton(icon_name)
            .large()
            .square()
            .subtle()
            .checkable()
            .tooltip(tip)
            .on_click(lambda k=key: select(k))
        )
        buttons[key] = button
        sidebar.add_widget(button)

    select("home")
    return sidebar


def build_window(app: KireiApp) -> KireiWindow:
    window = KireiWindow(title="KireiUI Gallery", width=1180, height=760)

    pages = KireiStack()
    pages.add_page("home", _wrap_in_scroll(build_home_page()))
    pages.add_page("widgets", _wrap_in_scroll(build_widgets_page()))
    pages.add_page("containers", _wrap_in_scroll(build_containers_page()))
    pages.add_page("feedback", _wrap_in_scroll(build_feedback_page(window)))
    pages.add_page("about", _wrap_in_scroll(build_about_page()))
    pages.current("home")

    sidebar = _build_icon_sidebar(pages)

    topbar = KireiTopBar("KireiUI Gallery").trailing(
        KireiHStack().spacing(8).add(KireiButton("Primary action").primary())
    )

    body = KireiHStack().spacing(0).add(sidebar).add(pages, stretch=1)

    root = KireiVStack().spacing(0).add(topbar).add(body, stretch=1)

    window.content(root)
    _ = app  # keep parameter referenced for clarity
    return window


def main() -> int:
    app = KireiApp(qss_dirs=["styles/neutral_dark"])
    window = build_window(app)
    window.show()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
