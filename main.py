from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from kirei_ui import KireiApp, KireiWindow


def main() -> int:
    app = KireiApp(
        application_name="KireiUI Demo",
        organization_name="KireiUI",
    )

    window = KireiWindow(
        title="KireiUI Window Test",
        width=900,
        height=600,
    )

    label = QLabel("Hello KireiUI")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("""
        QLabel {
            font-size: 28px;
            font-weight: 600;
            color: #1f2937;
            background-color: #f7f8fa;
        }
    """)

    window.set_content(label)
    window.show()

    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
