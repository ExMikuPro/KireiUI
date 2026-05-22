from kirei_ui import (
    KireiApp,
    KireiButton,
    KireiCheckbox,
    KireiComboBox,
    KireiForm,
    KireiHStack,
    KireiInput,
    KireiPassword,
    KireiRadio,
    KireiText,
    KireiTextarea,
    KireiTitle,
    KireiVStack,
    KireiWindow,
)


def main() -> int:
    app = KireiApp()

    root = (
        KireiVStack()
        .padding(32)
        .spacing(16)
        .add(KireiTitle("KireiUI Form Demo"))
        .add(KireiText("This page demonstrates basic KireiUI controls."))
        .add(
            KireiForm()
            .spacing(12)
            .add_row("Username", KireiInput().placeholder("Enter username").clearable())
            .add_row("Password", KireiPassword().placeholder("Enter password"))
            .add_row("Bio", KireiTextarea().placeholder("Write something..."))
            .add_row("Remember me", KireiCheckbox("Enabled").checked())
            .add_row(
                "Role",
                KireiComboBox().add_items(["User", "Admin", "Guest"]).current("User"),
            )
            .add_row(
                "Status",
                KireiHStack().spacing(8).add(KireiRadio("Active").checked()).add(KireiRadio("Paused")),
            )
        )
        .add(
            KireiHStack()
            .stretch()
            .add(KireiButton("Cancel").subtle())
            .add(KireiButton("Submit").primary().on_click(lambda: print("submit")))
        )
    )

    window = KireiWindow().title("KireiUI Form Demo").size(900, 600).content(root)
    window.show()

    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
