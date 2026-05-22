from __future__ import annotations

from PySide6.QtWidgets import QApplication
from typing_extensions import Self


class KireiMotionMixin:
    _animated: bool | None = None
    _animation_duration: int | None = None

    def animated(self, value: bool = True) -> Self:
        self._animated = value
        return self

    def animation_duration(self, duration: int) -> Self:
        self._animation_duration = max(0, int(duration))
        return self

    def should_animate(self, animated: bool | None = None) -> bool:
        if animated is not None:
            return animated

        instance_value = getattr(self, "_animated", None)
        if instance_value is not None:
            return bool(instance_value)

        app = QApplication.instance()
        if app is None:
            return True

        app_value = getattr(app, "enable_motion", None)
        if app_value is None:
            return True
        return bool(app_value)

    def resolved_animation_duration(self, duration: int | None = None) -> int:
        if duration is not None:
            return max(0, int(duration))

        instance_duration = getattr(self, "_animation_duration", None)
        if instance_duration is not None:
            return max(0, int(instance_duration))

        app = QApplication.instance()
        if app is None:
            return 180

        app_duration = getattr(app, "motion_duration", None)
        if app_duration is None:
            return 180

        return max(0, int(app_duration))
