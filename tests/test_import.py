from kirei_ui import (
    KireiCheckbox,
    KireiComboBox,
    KireiDivider,
    KireiInput,
    KireiLabel,
    KireiPassword,
    KireiRadio,
    KireiText,
    KireiTextarea,
    KireiTitle,
)


def test_new_widget_exports() -> None:
    assert KireiLabel is not None
    assert KireiTitle is not None
    assert KireiText is not None
    assert KireiInput is not None
    assert KireiTextarea is not None
    assert KireiPassword is not None
    assert KireiCheckbox is not None
    assert KireiRadio is not None
    assert KireiComboBox is not None
    assert KireiDivider is not None
