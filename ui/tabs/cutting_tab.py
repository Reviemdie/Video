from __future__ import annotations

from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class CuttingTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.input_path = QLineEdit()
        self.output_dir = QLineEdit()
        self.base_name = QLineEdit("segment")
        self.segment_duration = QSpinBox()
        self.segment_duration.setRange(1, 24 * 3600)
        self.segment_duration.setValue(60)
        self.fps = QSpinBox()
        self.fps.setRange(0, 240)
        self.fps.setValue(0)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        form.addRow("Input video", self._path_picker(self.input_path, True))
        form.addRow("Output folder", self._path_picker(self.output_dir, False))
        form.addRow("Output base name", self.base_name)
        form.addRow("Segment duration (sec)", self.segment_duration)
        form.addRow("FPS (0 = source)", self.fps)

        layout.addWidget(QLabel("Load a source video and configure slicing."))
        layout.addLayout(form)
        layout.addStretch()

    def _path_picker(self, target: QLineEdit, file_mode: bool) -> QWidget:
        wrapper = QWidget()
        h = QHBoxLayout(wrapper)
        h.setContentsMargins(0, 0, 0, 0)
        button = QPushButton("Browse")

        def pick() -> None:
            if file_mode:
                value, _ = QFileDialog.getOpenFileName(self, "Select video")
            else:
                value = QFileDialog.getExistingDirectory(self, "Select output folder")
            if value:
                target.setText(value)

        button.clicked.connect(pick)
        h.addWidget(target)
        h.addWidget(button)
        return wrapper
