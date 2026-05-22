from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from PySide6.QtWidgets import QApplication
from typing_extensions import Self

from kirei_ui.theme import build_qss, load_qss_file


class KireiApp(QApplication):
    """KireiUI application instance.

    This class wraps QApplication and provides a cleaner API for KireiUI users.
    """

    def __init__(
        self,
        argv: list[str] | Sequence[str] | None = None,
        *,
        theme: str | None = "base",
        qss_dirs: list[str | Path] | None = None,
        qss_files: list[str | Path] | None = None,
        recursive: bool = False,
        extra_qss: str | None = None,
        enable_motion: bool = True,
        motion_duration: int = 180,
        application_name: str = "KireiUI App",
        organization_name: str = "KireiUI",
    ) -> None:
        super().__init__(list(argv) if argv is not None else sys.argv)
        self.enable_motion = enable_motion
        self.motion_duration = motion_duration

        self.setApplicationName(application_name)
        self.setOrganizationName(organization_name)

        self.set_theme(
            theme=theme,
            qss_dirs=qss_dirs,
            qss_files=qss_files,
            recursive=recursive,
            extra_qss=extra_qss,
        )

    def set_theme(
        self,
        theme: str | None = "base",
        qss_dirs: list[str | Path] | None = None,
        qss_files: list[str | Path] | None = None,
        recursive: bool = False,
        extra_qss: str | None = None,
    ) -> Self:
        """Rebuild and apply the application stylesheet."""
        self.setStyleSheet(
            build_qss(
                theme=theme,
                qss_dirs=qss_dirs,
                qss_files=qss_files,
                recursive=recursive,
                extra_qss=extra_qss,
            )
        )
        return self

    def theme(
        self,
        theme: str | None = "base",
        qss_dirs: list[str | Path] | None = None,
        qss_files: list[str | Path] | None = None,
        recursive: bool = False,
        extra_qss: str | None = None,
    ) -> Self:
        return self.set_theme(
            theme=theme,
            qss_dirs=qss_dirs,
            qss_files=qss_files,
            recursive=recursive,
            extra_qss=extra_qss,
        )

    def load_qss(self, path: str | Path, append: bool = True) -> Self:
        """Load user QSS from file path.

        append=True appends to current stylesheet.
        append=False replaces current stylesheet.
        """
        qss = load_qss_file(path).strip()
        if not qss:
            return self

        if append:
            current = self.styleSheet().strip()
            if current:
                self.setStyleSheet(f"{current}\n\n{qss}")
            else:
                self.setStyleSheet(qss)
            return self

        self.setStyleSheet(qss)
        return self

    def set_motion_enabled(self, value: bool = True) -> Self:
        self.enable_motion = value
        return self

    def set_motion_duration(self, value: int = 180) -> Self:
        self.motion_duration = max(0, int(value))
        return self

    def run(self) -> int:
        """Start the Qt event loop."""
        return self.exec()
