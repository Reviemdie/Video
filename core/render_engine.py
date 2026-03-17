from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from core.models import ProjectSettings


class RenderEngine:
    def run_ffmpeg(self, command: list[str]) -> None:
        proc = subprocess.run(command, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {proc.stderr}")

    def probe_duration(self, input_file: str) -> float:
        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_file,
        ]
        proc = subprocess.run(command, check=True, capture_output=True, text=True)
        return float(proc.stdout.strip())

    def build_video_filters(self, settings: ProjectSettings) -> str:
        filters: list[str] = []
        if settings.speed != 1.0:
            filters.append(f"setpts={1/settings.speed:.4f}*PTS")
        if settings.orientation == "vertical":
            if settings.blur.enabled:
                blur = settings.blur
                filters.append(
                    "split=2[fg][bg];"
                    f"[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
                    f"gblur=sigma={blur.intensity},"
                    f"eq=contrast={blur.contrast}:saturation={blur.saturation},"
                    f"colorchannelmixer=aa={1 - blur.overlay_darkness}[bg2];"
                    "[fg]scale=1080:1920:force_original_aspect_ratio=decrease[fg2];"
                    "[bg2][fg2]overlay=(W-w)/2:(H-h)/2"
                )
            else:
                filters.append("scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2")
        return ",".join(f for f in filters if f)

    def build_output_path(self, output_dir: str, base_name: str, index: int) -> str:
        return str(Path(output_dir) / f"{base_name}{index:03d}.mp4")

    def to_shell(self, command: list[str]) -> str:
        return " ".join(shlex.quote(part) for part in command)
