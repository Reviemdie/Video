from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QFormLayout, QSpinBox, QVBoxLayout, QWidget


class SettingsTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.device = QComboBox(); self.device.addItems(["cpu", "gpu"])
        self.codec = QComboBox(); self.codec.addItems(["libx264", "libx265", "h264_nvenc"])
        self.crf = QSpinBox(); self.crf.setRange(0, 51); self.crf.setValue(20)
        self.preset = QComboBox(); self.preset.addItems(["ultrafast", "fast", "medium", "slow"])

        form.addRow("Render device", self.device)
        form.addRow("Codec", self.codec)
        form.addRow("CRF", self.crf)
        form.addRow("Preset", self.preset)

        layout.addLayout(form)
        layout.addStretch()
