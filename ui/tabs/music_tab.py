from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MusicTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.enabled = QCheckBox("Enable background music")
        self.path = QLineEdit()
        browse = QPushButton("Browse")
        browse.clicked.connect(self._browse)
        wrapper = QWidget()
        h = QHBoxLayout(wrapper)
        h.setContentsMargins(0, 0, 0, 0)
        h.addWidget(self.path)
        h.addWidget(browse)

        self.loop = QCheckBox("Loop")
        self.loop.setChecked(True)
        self.trim_start = QDoubleSpinBox(); self.trim_start.setRange(0, 99999)
        self.trim_end = QDoubleSpinBox(); self.trim_end.setRange(0, 99999)
        self.music_volume = QDoubleSpinBox(); self.music_volume.setRange(0, 2); self.music_volume.setValue(0.5)
        self.original_volume = QDoubleSpinBox(); self.original_volume.setRange(0, 2); self.original_volume.setValue(1)
        self.fade_in = QDoubleSpinBox(); self.fade_in.setRange(0, 30)
        self.fade_out = QDoubleSpinBox(); self.fade_out.setRange(0, 30)

        form.addRow("", self.enabled)
        form.addRow("Music file", wrapper)
        form.addRow("", self.loop)
        form.addRow("Trim start", self.trim_start)
        form.addRow("Trim end", self.trim_end)
        form.addRow("Music volume", self.music_volume)
        form.addRow("Original volume", self.original_volume)
        form.addRow("Fade in", self.fade_in)
        form.addRow("Fade out", self.fade_out)

        layout.addLayout(form)
        layout.addStretch()

    def _browse(self) -> None:
        value, _ = QFileDialog.getOpenFileName(self, "Select music")
        if value:
            self.path.setText(value)
