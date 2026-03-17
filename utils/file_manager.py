from __future__ import annotations

from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}


def is_supported_video(path: str) -> bool:
    return Path(path).suffix.lower() in VIDEO_EXTENSIONS


def is_supported_image(path: str) -> bool:
    return Path(path).suffix.lower() in IMAGE_EXTENSIONS


def is_supported_audio(path: str) -> bool:
    return Path(path).suffix.lower() in AUDIO_EXTENSIONS
