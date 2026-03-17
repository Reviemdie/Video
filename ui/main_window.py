from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.models import BannerSettings, BlurSettings, MusicSettings, ProjectSettings, RenderSettings, SubtitleSettings
from core.video_processor import VideoProcessor
from ui.tabs.banners_tab import BannersTab
from ui.tabs.cutting_tab import CuttingTab
from ui.tabs.format_tab import FormatTab
from ui.tabs.music_tab import MusicTab
from ui.tabs.presets_tab import PresetsTab
from ui.tabs.settings_tab import SettingsTab
from ui.tabs.subtitles_tab import SubtitlesTab
from utils.preset_manager import PresetManager


class Worker(QThread):
    progress = Signal(int, int)
    done = Signal(str)
    failed = Signal(str)

    def __init__(self, processor: VideoProcessor, settings: ProjectSettings) -> None:
        super().__init__()
        self.processor = processor
        self.settings = settings

    def run(self) -> None:
        try:
            stats = self.processor.process(self.settings, self.progress.emit)
            self.done.emit(f"Done: {stats.completed_segments}/{stats.total_segments} segments")
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self, presets_dir: Path) -> None:
        super().__init__()
        self.setWindowTitle("Video Cutter Pro")
        self.resize(1080, 760)

        self.processor = VideoProcessor()
        self.worker: Worker | None = None
        self.preset_manager = PresetManager(presets_dir)

        self.tabs = QTabWidget()
        self.cutting_tab = CuttingTab()
        self.format_tab = FormatTab()
        self.banners_tab = BannersTab()
        self.subtitles_tab = SubtitlesTab()
        self.music_tab = MusicTab()
        self.settings_tab = SettingsTab()
        self.presets_tab = PresetsTab(self.preset_manager, self.apply_settings, self.collect_settings)

        self.tabs.addTab(self.cutting_tab, "Cutting")
        self.tabs.addTab(self.format_tab, "Format")
        self.tabs.addTab(self.banners_tab, "Banners")
        self.tabs.addTab(self.subtitles_tab, "Subtitles")
        self.tabs.addTab(self.music_tab, "Music")
        self.tabs.addTab(self.presets_tab, "Presets")
        self.tabs.addTab(self.settings_tab, "Settings")

        self.progress = QProgressBar()
        self.status_label = QLabel("Ready")

        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_processing)
        self.stop_btn.clicked.connect(self.stop_processing)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.tabs)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        self.setCentralWidget(central)

    def collect_settings(self) -> ProjectSettings:
        return ProjectSettings(
            input_file=self.cutting_tab.input_path.text().strip(),
            output_dir=self.cutting_tab.output_dir.text().strip(),
            output_base_name=self.cutting_tab.base_name.text().strip() or "segment",
            segment_duration=self.cutting_tab.segment_duration.value(),
            fps=self.cutting_tab.fps.value(),
            orientation=self.format_tab.orientation.currentText(),
            speed=self.format_tab.speed.value(),
            blur=BlurSettings(
                enabled=self.format_tab.blur_enabled.isChecked(),
                intensity=self.format_tab.blur_intensity.value(),
                scale=self.format_tab.blur_scale.value(),
                overlay_darkness=self.format_tab.overlay_darkness.value(),
                contrast=self.format_tab.contrast.value(),
                saturation=self.format_tab.saturation.value(),
            ),
            banners=[
                BannerSettings(
                    path=self.banners_tab.path.text().strip(),
                    x=self.banners_tab.x.value(),
                    y=self.banners_tab.y.value(),
                    width=self.banners_tab.width.value(),
                    height=self.banners_tab.height.value(),
                    opacity=self.banners_tab.opacity.value(),
                    animation=self.banners_tab.animation.currentText(),
                )
            ]
            if self.banners_tab.path.text().strip()
            else [],
            subtitles=SubtitleSettings(
                enabled=self.subtitles_tab.enabled.isChecked(),
                model=self.subtitles_tab.model.currentText(),
                font=self.subtitles_tab.font.text().strip(),
                color=self.subtitles_tab.color.text().strip(),
                size=self.subtitles_tab.size.value(),
                position=self.subtitles_tab.position.currentText(),
                word_highlight=self.subtitles_tab.word_highlight.isChecked(),
            ),
            music=MusicSettings(
                enabled=self.music_tab.enabled.isChecked(),
                path=self.music_tab.path.text().strip(),
                loop=self.music_tab.loop.isChecked(),
                trim_start=self.music_tab.trim_start.value(),
                trim_end=self.music_tab.trim_end.value(),
                music_volume=self.music_tab.music_volume.value(),
                original_volume=self.music_tab.original_volume.value(),
                fade_in=self.music_tab.fade_in.value(),
                fade_out=self.music_tab.fade_out.value(),
            ),
            render=RenderSettings(
                device=self.settings_tab.device.currentText(),
                codec=self.settings_tab.codec.currentText(),
                crf=self.settings_tab.crf.value(),
                preset=self.settings_tab.preset.currentText(),
            ),
        )

    def apply_settings(self, settings: ProjectSettings) -> None:
        self.cutting_tab.input_path.setText(settings.input_file)
        self.cutting_tab.output_dir.setText(settings.output_dir)
        self.cutting_tab.base_name.setText(settings.output_base_name)
        self.cutting_tab.segment_duration.setValue(settings.segment_duration)
        self.cutting_tab.fps.setValue(settings.fps)

        self.format_tab.orientation.setCurrentText(settings.orientation)
        self.format_tab.speed.setValue(settings.speed)
        self.format_tab.blur_enabled.setChecked(settings.blur.enabled)
        self.format_tab.blur_intensity.setValue(settings.blur.intensity)
        self.format_tab.blur_scale.setValue(settings.blur.scale)
        self.format_tab.overlay_darkness.setValue(settings.blur.overlay_darkness)
        self.format_tab.contrast.setValue(settings.blur.contrast)
        self.format_tab.saturation.setValue(settings.blur.saturation)

        if settings.banners:
            banner = settings.banners[0]
            self.banners_tab.path.setText(banner.path)
            self.banners_tab.x.setValue(banner.x)
            self.banners_tab.y.setValue(banner.y)
            self.banners_tab.width.setValue(banner.width)
            self.banners_tab.height.setValue(banner.height)
            self.banners_tab.opacity.setValue(banner.opacity)
            self.banners_tab.animation.setCurrentText(banner.animation)

        self.subtitles_tab.enabled.setChecked(settings.subtitles.enabled)
        self.subtitles_tab.model.setCurrentText(settings.subtitles.model)
        self.subtitles_tab.font.setText(settings.subtitles.font)
        self.subtitles_tab.color.setText(settings.subtitles.color)
        self.subtitles_tab.size.setValue(settings.subtitles.size)
        self.subtitles_tab.position.setCurrentText(settings.subtitles.position)
        self.subtitles_tab.word_highlight.setChecked(settings.subtitles.word_highlight)

        self.music_tab.enabled.setChecked(settings.music.enabled)
        self.music_tab.path.setText(settings.music.path)
        self.music_tab.loop.setChecked(settings.music.loop)
        self.music_tab.trim_start.setValue(settings.music.trim_start)
        self.music_tab.trim_end.setValue(settings.music.trim_end)
        self.music_tab.music_volume.setValue(settings.music.music_volume)
        self.music_tab.original_volume.setValue(settings.music.original_volume)
        self.music_tab.fade_in.setValue(settings.music.fade_in)
        self.music_tab.fade_out.setValue(settings.music.fade_out)

        self.settings_tab.device.setCurrentText(settings.render.device)
        self.settings_tab.codec.setCurrentText(settings.render.codec)
        self.settings_tab.crf.setValue(settings.render.crf)
        self.settings_tab.preset.setCurrentText(settings.render.preset)

    def start_processing(self) -> None:
        settings = self.collect_settings()
        if not settings.input_file or not settings.output_dir:
            QMessageBox.warning(self, "Required", "Please select input file and output folder")
            return

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress.setValue(0)
        self.status_label.setText("Processing...")

        self.worker = Worker(self.processor, settings)
        self.worker.progress.connect(self._on_progress)
        self.worker.done.connect(self._on_done)
        self.worker.failed.connect(self._on_failed)
        self.worker.start()

    def stop_processing(self) -> None:
        self.processor.request_stop()
        self.status_label.setText("Stopping...")

    def _on_progress(self, current: int, total: int) -> None:
        pct = int((current / total) * 100) if total else 0
        self.progress.setValue(pct)
        self.status_label.setText(f"Processed {current}/{total}")

    def _on_done(self, message: str) -> None:
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText(message)
        self.presets_tab.refresh()

    def _on_failed(self, error: str) -> None:
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Failed")
        QMessageBox.critical(self, "Error", error)
