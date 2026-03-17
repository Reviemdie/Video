from __future__ import annotations

from core.models import MusicSettings


class AudioProcessor:
    def build_audio_filters(self, music: MusicSettings) -> str:
        filters: list[str] = []
        if music.fade_in > 0:
            filters.append(f"afade=t=in:st=0:d={music.fade_in}")
        if music.fade_out > 0:
            filters.append(f"afade=t=out:st=0:d={music.fade_out}")
        if music.music_volume != 1.0:
            filters.append(f"volume={music.music_volume}")
        return ",".join(filters)
