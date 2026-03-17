from __future__ import annotations

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from utils.preset_manager import PresetManager


class PresetsTab(QWidget):
    def __init__(self, manager: PresetManager, on_load, on_save_current) -> None:
        super().__init__()
        self.manager = manager
        self.on_load = on_load
        self.on_save_current = on_save_current
        self.list = QListWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.list)

        row = QHBoxLayout()
        for title, handler in [
            ("Save", self.save_new),
            ("Update", self.update_selected),
            ("Load", self.load_selected),
            ("Delete", self.delete_selected),
            ("Import", self.import_preset),
            ("Export", self.export_preset),
        ]:
            btn = QPushButton(title)
            btn.clicked.connect(handler)
            row.addWidget(btn)
        layout.addLayout(row)
        self.refresh()

    def refresh(self) -> None:
        self.list.clear()
        self.list.addItems(self.manager.list_presets())

    def _selected(self) -> str | None:
        item = self.list.currentItem()
        return item.text() if item else None

    def save_new(self) -> None:
        name, ok = QInputDialog.getText(self, "Preset", "Preset name")
        if ok and name.strip():
            self.manager.save_preset(name.strip(), self.on_save_current())
            self.refresh()

    def update_selected(self) -> None:
        name = self._selected()
        if not name:
            return
        self.manager.save_preset(name, self.on_save_current())
        self.refresh()

    def load_selected(self) -> None:
        name = self._selected()
        if not name:
            return
        self.on_load(self.manager.load_preset(name))

    def delete_selected(self) -> None:
        name = self._selected()
        if not name:
            return
        self.manager.delete_preset(name)
        self.refresh()

    def import_preset(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Import preset", filter="JSON (*.json)")
        if path:
            name = self.manager.import_preset(path)
            QMessageBox.information(self, "Imported", f"Preset '{name}' imported")
            self.refresh()

    def export_preset(self) -> None:
        name = self._selected()
        if not name:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export preset", f"{name}.json", "JSON (*.json)")
        if path:
            self.manager.export_preset(name, path)
