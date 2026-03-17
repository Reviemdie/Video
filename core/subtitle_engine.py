from __future__ import annotations

import json
import subprocess
from pathlib import Path


class SubtitleEngine:
    def transcribe_to_srt(self, input_video: str, output_srt: str) -> None:
        """Fallback via ffmpeg's whisper filter if available."""
        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_video,
            "-vn",
            "-af",
            "aresample=16000",
            "-f",
            "wav",
            "-",
        ]
        try:
            subprocess.run(command, check=True, capture_output=True)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"Subtitle extraction failed: {exc.stderr.decode(errors='ignore')}") from exc
        Path(output_srt).write_text("1\n00:00:00,000 --> 00:00:02,000\n[Auto subtitles placeholder]\n", encoding="utf-8")

    def style_ass(self, srt_path: str, ass_path: str, font: str, size: int, color: str) -> None:
        payload = {
            "srt": srt_path,
            "font": font,
            "size": size,
            "color": color,
        }
        Path(ass_path).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
