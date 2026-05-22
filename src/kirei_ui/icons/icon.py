from __future__ import annotations

from PySide6.QtGui import QIcon

from kirei_ui.icons.registry import KireiIconRegistry


class KireiIcon:
    """Static helpers for resolving Fluent icon names to :class:`QIcon`.

    Icons are resolved via :class:`KireiIconRegistry`, which loads the
    bundled ``manifest.json`` lazily on first access. The class is a
    namespace of static helpers — do not instantiate.
    """

    @staticmethod
    def get(name: str, style: str = "regular", size: int = 20, *, strict: bool = False) -> QIcon:
        """Alias of :meth:`qicon` kept for API symmetry."""
        return KireiIcon.qicon(name, style=style, size=size, strict=strict)

    @staticmethod
    def qicon(name: str, style: str = "regular", size: int = 20, *, strict: bool = False) -> QIcon:
        """Resolve ``name`` to a :class:`QIcon`.

        Args:
            name: Fluent icon name (e.g. ``"save"`` or ``"chevron-down"``).
            style: ``"regular"`` or ``"filled"``. Falls back to the other
                style when the requested one is missing.
            size: Preferred pixel size. The closest available size is used.
            strict: When True, raise :class:`KeyError` if the name cannot be
                resolved at all. Default returns an empty :class:`QIcon`.
        """
        icon_path = KireiIconRegistry.path(name, style=style, size=size, strict=strict)
        if not icon_path:
            return QIcon()
        return QIcon(icon_path)


def icon(name: str, style: str = "regular", size: int = 20, *, strict: bool = False) -> QIcon:
    """Module-level shortcut for :meth:`KireiIcon.qicon`."""
    return KireiIcon.qicon(name, style=style, size=size, strict=strict)
