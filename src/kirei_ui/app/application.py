from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from PySide6.QtWidgets import QApplication
from typing_extensions import Self

from kirei_ui.theme import build_qss, load_qss_file


class KireiApp(QApplication):
    """KireiUI application instance.

    Subclasses :class:`QApplication` to bundle three pieces of setup:

    - The application / organization name (used by Qt for settings).
    - The composed stylesheet (built from the requested theme, user
      QSS directories and files, and an optional inline override).
    - Animation defaults (``enable_motion`` and ``motion_duration``)
      that :class:`KireiMotionMixin` reads when an instance does not
      override them.

    Pass an explicit ``argv`` for testing; otherwise ``sys.argv`` is
    used. Call :meth:`run` to start the Qt event loop.
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
        """Create the application.

        Args:
            argv: Command-line arguments. ``None`` falls back to ``sys.argv``.
            theme: Built-in theme name (only ``"base"`` ships today). ``None`` skips it.
            qss_dirs: Directories to scan for ``*.qss`` files.
            qss_files: Specific QSS files to load (in order, after directory scans).
            recursive: When True, ``qss_dirs`` is walked recursively.
            extra_qss: Inline QSS appended last (highest priority).
            enable_motion: App-level default for animation enablement.
            motion_duration: App-level default animation duration in milliseconds.
            application_name: Qt application name (settings / window class).
            organization_name: Qt organization name (settings).
        """
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
        """Rebuild and apply the application stylesheet.

        Replaces the current stylesheet with a fresh build from
        :func:`build_qss`. Use :meth:`load_qss` instead to append a
        single file without rebuilding the theme.
        """
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
        """Chainable :meth:`set_theme`."""
        return self.set_theme(
            theme=theme,
            qss_dirs=qss_dirs,
            qss_files=qss_files,
            recursive=recursive,
            extra_qss=extra_qss,
        )

    def load_qss(self, path: str | Path, append: bool = True) -> Self:
        """Load user QSS from a file path.

        Args:
            path: File system path to a ``.qss`` file.
            append: When True (default), the file's contents are
                appended to the current stylesheet. When False, they
                replace it. Empty / whitespace-only files are no-ops.
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
        """Set the app-level default for whether widgets animate."""
        self.enable_motion = value
        return self

    def set_motion_duration(self, value: int = 180) -> Self:
        """Set the app-level default animation duration (ms). Negative values clamp to 0."""
        self.motion_duration = max(0, int(value))
        return self

    def run(self) -> int:
        """Start the Qt event loop. Returns the application's exit code."""
        return self.exec()
