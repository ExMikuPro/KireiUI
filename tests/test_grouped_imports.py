from kirei_ui.app import KireiApp, KireiWindow
from kirei_ui.data import KireiList, KireiTable, KireiTree
from kirei_ui.desktop import KireiMenuBar, KireiStatusBar, KireiSystemTray
from kirei_ui.feedback import KireiAlert, KireiBadge, KireiProgress
from kirei_ui.inputs import KireiButton, KireiCheckbox, KireiInput
from kirei_ui.layout import KireiGrid, KireiHStack, KireiVStack
from kirei_ui.navigation import KireiSidebar, KireiTabs, KireiTopBar
from kirei_ui.overlay import KireiDialog, KireiDrawer, KireiTooltip
from kirei_ui.theme import KireiStyle, KireiTheme, KireiTokens


def test_grouped_imports_available() -> None:
    assert KireiApp is not None
    assert KireiWindow is not None
    assert KireiHStack is not None
    assert KireiVStack is not None
    assert KireiGrid is not None
    assert KireiButton is not None
    assert KireiInput is not None
    assert KireiCheckbox is not None
    assert KireiAlert is not None
    assert KireiBadge is not None
    assert KireiProgress is not None
    assert KireiTopBar is not None
    assert KireiSidebar is not None
    assert KireiTabs is not None
    assert KireiDialog is not None
    assert KireiDrawer is not None
    assert KireiTooltip is not None
    assert KireiTable is not None
    assert KireiList is not None
    assert KireiTree is not None
    assert KireiMenuBar is not None
    assert KireiStatusBar is not None
    assert KireiSystemTray is not None
    assert KireiTheme is not None
    assert KireiTokens is not None
    assert KireiStyle is not None
