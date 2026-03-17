from __future__ import annotations

from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QWidget,
    QComboBox,
)


class BannersTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.path = QLineEdit()
        browse = QPushButton("Browse")
        browse.clicked.connect(self._browse)
        path_wrap = QWidget()
        path_layout = QHBoxLayout(path_wrap)
        path_layout.setContentsMargins(0, 0, 0, 0)
        path_layout.addWidget(self.path)
        path_layout.addWidget(browse)

        self.x = QSpinBox(); self.x.setRange(-2000, 4000)
        self.y = QSpinBox(); self.y.setRange(-2000, 4000)
        self.width = QSpinBox(); self.width.setRange(1, 5000); self.width.setValue(320)
        self.height = QSpinBox(); self.height.setRange(1, 5000); self.height.setValue(180)
        self.opacity = QDoubleSpinBox(); self.opacity.setRange(0.0, 1.0); self.opacity.setValue(1.0)
        self.animation = QComboBox(); self.animation.addItems(["none", "fade", "slide-left", "slide-up"])

        form.addRow("Banner file", path_wrap)
        form.addRow("X", self.x)
        form.addRow("Y", self.y)
        form.addRow("Width", self.width)
        form.addRow("Height", self.height)
        form.addRow("Opacity", self.opacity)
        form.addRow("Animation", self.animation)

        layout.addLayout(form)
        layout.addStretch()

    def _browse(self) -> None:
        value, _ = QFileDialog.getOpenFileName(self, "Select banner")
        if value:
            self.path.setText(value)
