"""Centralized text strings used by built-in components.

KireiUI does not (yet) ship a real i18n system. This module is the single source
of truth for default labels so users can override them in one place::

    from kirei_ui.locale import KireiTexts

    KireiTexts.button_loading = "Working..."
    KireiTexts.confirm_ok = "Yes"

Components read these values lazily on each render so live updates apply.
"""

from __future__ import annotations


class KireiTexts:
    """Default user-facing strings used by built-in components.

    All entries are class attributes; reassign to override globally.
    """

    button_loading: str = "处理中..."
    spinner_default: str = "Loading..."
    confirm_ok: str = "Confirm"
    confirm_cancel: str = "Cancel"


__all__ = ["KireiTexts"]
