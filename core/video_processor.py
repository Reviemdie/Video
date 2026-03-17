from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from core.audio_processor import AudioProcessor
from core.models import ProjectSettings
from core.render_engine import RenderEngine


@dataclass
class ProcessStats:
    total_segments: int = 0
    completed_segments: int = 0


class VideoProcessor:
    def __init__(self) -> None:
        self.render = RenderEngine()
        self.audio = AudioProcessor()
        self._stop_requested = False

    def request_stop(self) -> None:
        self._stop_requested = True

    def process(self, settings: ProjectSettings, on_progress: Callable[[int, int], None] | None = None) -> ProcessStats:
        settings.validate_paths()
        duration = self.render.probe_duration(settings.input_file)
        segment = max(1, settings.segment_duration)
        total = int(duration // segment) + (1 if duration % segment else 0)

        stats = ProcessStats(total_segments=total)
        filters = self.render.build_video_filters(settings)

        for idx in range(total):
            if self._stop_requested:
                break
            start = idx * segment
            out_path = self.render.build_output_path(settings.output_dir, settings.output_base_name, idx + 1)
            command = ["ffmpeg", "-y", "-ss", str(start), "-t", str(segment), "-i", settings.input_file]

            if settings.music.enabled and settings.music.path:
                command += ["-stream_loop", "-1" if settings.music.loop else "0", "-i", settings.music.path]
                audio_filter = self.audio.build_audio_filters(settings.music)
                if audio_filter:
                    command += ["-filter:a", audio_filter]

            if filters:
                command += ["-vf", filters]

            if settings.fps > 0:
                command += ["-r", str(settings.fps)]

            command += ["-c:v", settings.render.codec, "-preset", settings.render.preset, "-crf", str(settings.render.crf), out_path]
            self.render.run_ffmpeg(command)

            stats.completed_segments += 1
            if on_progress:
                on_progress(stats.completed_segments, stats.total_segments)

        self._stop_requested = False
        return stats
