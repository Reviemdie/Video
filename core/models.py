from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass
class BlurSettings:
    enabled: bool = True
    intensity: int = 20
    scale: float = 1.2
    overlay_darkness: float = 0.2
    contrast: float = 1.0
    saturation: float = 1.0


@dataclass
class BannerSettings:
    path: str = ""
    x: int = 0
    y: int = 0
    width: int = 320
    height: int = 180
    opacity: float = 1.0
    animation: str = "none"


@dataclass
class SubtitleSettings:
    enabled: bool = False
    model: str = "tiny"
    font: str = "Arial"
    color: str = "#FFFFFF"
    size: int = 36
    position: str = "bottom"
    word_highlight: bool = True


@dataclass
class MusicSettings:
    enabled: bool = False
    path: str = ""
    loop: bool = True
    trim_start: float = 0.0
    trim_end: float = 0.0
    music_volume: float = 0.5
    original_volume: float = 1.0
    fade_in: float = 0.0
    fade_out: float = 0.0


@dataclass
class RenderSettings:
    device: str = "cpu"
    codec: str = "libx264"
    crf: int = 20
    preset: str = "medium"


@dataclass
class ProjectSettings:
    input_file: str = ""
    output_dir: str = ""
    output_base_name: str = "segment"
    segment_duration: int = 60
    fps: int = 0
    orientation: str = "horizontal"
    speed: float = 1.0
    blur: BlurSettings = field(default_factory=BlurSettings)
    banners: list[BannerSettings] = field(default_factory=list)
    subtitles: SubtitleSettings = field(default_factory=SubtitleSettings)
    music: MusicSettings = field(default_factory=MusicSettings)
    render: RenderSettings = field(default_factory=RenderSettings)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(payload: dict[str, Any]) -> "ProjectSettings":
        blur = BlurSettings(**payload.get("blur", {}))
        banners = [BannerSettings(**item) for item in payload.get("banners", [])]
        subtitles = SubtitleSettings(**payload.get("subtitles", {}))
        music = MusicSettings(**payload.get("music", {}))
        render = RenderSettings(**payload.get("render", {}))
        base = {k: v for k, v in payload.items() if k not in {"blur", "banners", "subtitles", "music", "render"}}
        return ProjectSettings(
            **base,
            blur=blur,
            banners=banners,
            subtitles=subtitles,
            music=music,
            render=render,
        )

    def validate_paths(self) -> None:
        if self.input_file and not Path(self.input_file).exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        if self.output_dir:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
