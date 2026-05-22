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
        .add(KireiTitle("KireiUI 表单示例"))
        .add(KireiText("本页面展示 KireiUI 的基础表单控件。"))
        .add(
            KireiForm()
            .spacing(12)
            .add_row("用户名", KireiInput().placeholder("请输入用户名").clearable())
            .add_row("密码", KireiPassword().placeholder("请输入密码"))
            .add_row("简介", KireiTextarea().placeholder("写点什么..."))
            .add_row("记住我", KireiCheckbox("启用").checked())
            .add_row(
                "角色",
                KireiComboBox().add_items(["用户", "管理员", "访客"]).current("用户"),
            )
            .add_row(
                "状态",
                KireiHStack().spacing(8).add(KireiRadio("启用").checked()).add(KireiRadio("暂停")),
            )
        )
        .add(
            KireiHStack()
            .stretch()
            .add(KireiButton("取消").subtle())
            .add(KireiButton("提交").primary().on_click(lambda: print("提交")))
        )
    )

    window = KireiWindow().title("KireiUI 表单示例").size(900, 600).content(root)
    window.show()

    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
