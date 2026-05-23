from __future__ import annotations

import re
from typing import ClassVar

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from kirei_ui.icons.registry import KireiIconRegistry

_FLUENT_FILL_PATTERN = re.compile(r'fill="#212121"', re.IGNORECASE)
_DEFAULT_LIGHT_GLYPH = "#1E293B"


def _normalise_color(color: str | QColor | None) -> str | None:
    if color is None:
        return None
    if isinstance(color, QColor):
        return color.name(QColor.NameFormat.HexRgb)
    return str(color)


class KireiIcon:
    """Resolve Fluent icon names to :class:`QIcon`, recoloured for the active theme.

    Fluent SVGs ship with a hard-coded ``fill="#212121"``. :meth:`qicon`
    replaces that fill with the current theme glyph colour so icons
    stay legible on both light and dark surfaces. The recoloured
    pixmap is cached by ``(name, style, size, color)``; call
    :meth:`clear_cache` after swapping the icon set.

    The class is a namespace of static helpers — do not instantiate.
    """

    _default_color: ClassVar[str] = _DEFAULT_LIGHT_GLYPH
    _pixmap_cache: ClassVar[dict[tuple[str, str, int, str], QPixmap]] = {}

    @staticmethod
    def set_default_color(color: str | QColor | None) -> None:
        """Set the glyph colour applied when callers do not pass ``color``.

        Pass ``None`` to restore the bundled default. Cached pixmaps are
        kept — they are keyed on the resolved colour, not the default.
        """
        normalised = _normalise_color(color)
        KireiIcon._default_color = normalised or _DEFAULT_LIGHT_GLYPH

    @staticmethod
    def default_color() -> str:
        """Return the colour currently used when callers omit ``color``."""
        return KireiIcon._default_color

    @staticmethod
    def clear_cache() -> None:
        """Discard every cached recoloured pixmap."""
        KireiIcon._pixmap_cache.clear()

    @staticmethod
    def get(
        name: str,
        style: str = "regular",
        size: int = 20,
        *,
        color: str | QColor | None = None,
        strict: bool = False,
    ) -> QIcon:
        """Alias of :meth:`qicon` kept for API symmetry."""
        return KireiIcon.qicon(name, style=style, size=size, color=color, strict=strict)

    @staticmethod
    def qicon(
        name: str,
        style: str = "regular",
        size: int = 20,
        *,
        color: str | QColor | None = None,
        strict: bool = False,
    ) -> QIcon:
        """Resolve ``name`` to a :class:`QIcon` rendered in ``color``.

        Args:
            name: Fluent icon name (e.g. ``"save"`` or ``"chevron-down"``).
            style: ``"regular"`` or ``"filled"``. Falls back to the other
                style when the requested one is missing.
            size: Preferred pixel size. The closest available SVG size
                is used, then the SVG is re-rasterised to ``size``.
            color: Glyph colour as a ``"#RRGGBB"`` string or :class:`QColor`.
                When ``None`` the value from :meth:`default_color` is used,
                which is updated by the active theme.
            strict: When True, raise :class:`KeyError` if the name cannot
                be resolved at all. Default returns an empty :class:`QIcon`.
        """
        icon_path = KireiIconRegistry.path(name, style=style, size=size, strict=strict)
        if not icon_path:
            return QIcon()

        resolved_color = _normalise_color(color) or KireiIcon._default_color
        cache_key = (icon_path, style, int(size), resolved_color)
        cached = KireiIcon._pixmap_cache.get(cache_key)
        if cached is None:
            cached = _render_recoloured(icon_path, int(size), resolved_color)
            KireiIcon._pixmap_cache[cache_key] = cached

        icon = QIcon()
        icon.addPixmap(cached)
        return icon


def _render_recoloured(svg_path: str, size: int, color: str) -> QPixmap:
    with open(svg_path, encoding="utf-8") as handle:
        svg_text = handle.read()

    recoloured = _FLUENT_FILL_PATTERN.sub(f'fill="{color}"', svg_text)
    renderer = QSvgRenderer(QByteArray(recoloured.encode("utf-8")))

    pixmap = QPixmap(QSize(size, size))
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()

    return pixmap


def icon(
    name: str,
    style: str = "regular",
    size: int = 20,
    *,
    color: str | QColor | None = None,
    strict: bool = False,
) -> QIcon:
    """Module-level shortcut for :meth:`KireiIcon.qicon`."""
    return KireiIcon.qicon(name, style=style, size=size, color=color, strict=strict)
