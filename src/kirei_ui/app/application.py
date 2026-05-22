from __future__ import annotations

import sys
from collections.abc import Sequence

from PySide6.QtWidgets import QApplication


class KireiApp(QApplication):
    """KireiUI application instance.

    This class wraps QApplication and provides a cleaner API for KireiUI users.
    """

    def __init__(
        self,
        argv: Sequence[str] | None = None,
        *,
        application_name: str = "KireiUI App",
        organization_name: str = "KireiUI",
    ) -> None:
        super().__init__(list(argv) if argv is not None else sys.argv)

        self.setApplicationName(application_name)
        self.setOrganizationName(organization_name)

    def run(self) -> int:
        """Start the Qt event loop."""
        return self.exec()
