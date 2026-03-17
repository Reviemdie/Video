from __future__ import annotations

import json
from pathlib import Path

from core.models import ProjectSettings


class PresetManager:
    def __init__(self, presets_dir: Path) -> None:
        self.presets_dir = presets_dir
        self.presets_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, name: str) -> Path:
        safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip()
        if not safe:
            raise ValueError("Preset name cannot be empty")
        return self.presets_dir / f"{safe}.json"

    def list_presets(self) -> list[str]:
        return sorted(p.stem for p in self.presets_dir.glob("*.json"))

    def save_preset(self, name: str, settings: ProjectSettings) -> Path:
        path = self._file_path(name)
        path.write_text(json.dumps(settings.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def load_preset(self, name: str) -> ProjectSettings:
        path = self._file_path(name)
        payload = json.loads(path.read_text(encoding="utf-8"))
        return ProjectSettings.from_dict(payload)

    def delete_preset(self, name: str) -> None:
        self._file_path(name).unlink(missing_ok=True)

    def import_preset(self, source_path: str) -> str:
        src = Path(source_path)
        payload = json.loads(src.read_text(encoding="utf-8"))
        settings = ProjectSettings.from_dict(payload)
        target_name = src.stem
        self.save_preset(target_name, settings)
        return target_name

    def export_preset(self, name: str, dest_path: str) -> None:
        src = self._file_path(name)
        Path(dest_path).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
