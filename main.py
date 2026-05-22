from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from kirei_ui import KireiApp, KireiButton, KireiWindow


def main() -> int:
    app = KireiApp()
    # app = KireiApp(qss_files=["assets/app.qss"])
    # app.load_qss("assets/app.qss")

    root = QWidget()
    layout = QVBoxLayout(root)
    layout.setContentsMargins(32, 32, 32, 32)
    layout.setSpacing(16)

    row = QHBoxLayout()
    row.setSpacing(8)

    row.addWidget(KireiButton("Default"))
    row.addWidget(KireiButton("Primary").primary())
    row.addWidget(KireiButton("Link").link())
    row.addWidget(KireiButton("Subtle").subtle())
    row.addWidget(KireiButton("Danger").danger())
    row.addWidget(KireiButton("Warning").warning())
    row.addStretch()

    compact_row = QHBoxLayout()
    compact_row.setSpacing(8)

    compact_row.addWidget(KireiButton("Compact").compact())
    compact_row.addWidget(KireiButton("Compact Primary").primary().compact())
    compact_row.addStretch()

    layout.addLayout(row)
    layout.addLayout(compact_row)
    layout.addStretch()

    window = KireiWindow().title("KireiUI AUI Button Test").size(900, 600).content(root)
    window.show()

    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
