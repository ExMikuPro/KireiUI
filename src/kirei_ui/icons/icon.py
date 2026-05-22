from __future__ import annotations

from PySide6.QtGui import QIcon

from kirei_ui.icons.registry import KireiIconRegistry


class KireiIcon:
    @staticmethod
    def get(name: str, style: str = "regular", size: int = 20, *, strict: bool = False) -> QIcon:
        return KireiIcon.qicon(name, style=style, size=size, strict=strict)

    @staticmethod
    def qicon(name: str, style: str = "regular", size: int = 20, *, strict: bool = False) -> QIcon:
        icon_path = KireiIconRegistry.path(name, style=style, size=size, strict=strict)
        if not icon_path:
            return QIcon()
        return QIcon(icon_path)


def icon(name: str, style: str = "regular", size: int = 20, *, strict: bool = False) -> QIcon:
    return KireiIcon.qicon(name, style=style, size=size, strict=strict)
