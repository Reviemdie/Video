from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class FormatTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.orientation = QComboBox()
        self.orientation.addItems(["horizontal", "vertical"])
        self.speed = QDoubleSpinBox()
        self.speed.setRange(0.5, 4.0)
        self.speed.setSingleStep(0.1)
        self.speed.setValue(1.0)

        self.blur_enabled = QCheckBox("Enable blur background")
        self.blur_enabled.setChecked(True)
        self.blur_intensity = QSpinBox()
        self.blur_intensity.setRange(0, 100)
        self.blur_intensity.setValue(20)
        self.blur_scale = QDoubleSpinBox()
        self.blur_scale.setRange(1.0, 3.0)
        self.blur_scale.setValue(1.2)
        self.overlay_darkness = QDoubleSpinBox()
        self.overlay_darkness.setRange(0.0, 1.0)
        self.overlay_darkness.setValue(0.2)
        self.contrast = QDoubleSpinBox()
        self.contrast.setRange(0.1, 3.0)
        self.contrast.setValue(1.0)
        self.saturation = QDoubleSpinBox()
        self.saturation.setRange(0.0, 3.0)
        self.saturation.setValue(1.0)

        form.addRow("Orientation", self.orientation)
        form.addRow("Speed", self.speed)
        form.addRow("", self.blur_enabled)
        form.addRow("Blur intensity", self.blur_intensity)
        form.addRow("Background scale", self.blur_scale)
        form.addRow("Overlay darkness", self.overlay_darkness)
        form.addRow("Contrast", self.contrast)
        form.addRow("Saturation", self.saturation)

        layout.addLayout(form)
        layout.addStretch()
