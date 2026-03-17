from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QLineEdit, QSpinBox, QVBoxLayout, QWidget


class SubtitlesTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.enabled = QCheckBox("Enable AI subtitles")
        self.model = QComboBox(); self.model.addItems(["tiny", "base", "small", "medium"])
        self.font = QLineEdit("Arial")
        self.color = QLineEdit("#FFFFFF")
        self.size = QSpinBox(); self.size.setRange(10, 120); self.size.setValue(36)
        self.position = QComboBox(); self.position.addItems(["top", "center", "bottom"])
        self.word_highlight = QCheckBox("Word-by-word highlight")
        self.word_highlight.setChecked(True)

        form.addRow("", self.enabled)
        form.addRow("Model", self.model)
        form.addRow("Font", self.font)
        form.addRow("Color", self.color)
        form.addRow("Size", self.size)
        form.addRow("Position", self.position)
        form.addRow("", self.word_highlight)

        layout.addLayout(form)
        layout.addStretch()
