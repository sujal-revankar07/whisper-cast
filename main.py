import logging
from time import sleep
from .audio_capture import AudioCapture
from .transcription import TranscriptionEngine
from .hotkey_manager import HotkeyManager
from .utils import logger
class WhisperCastApp:
    def __init__(self):
        self.audio = AudioCapture()
        self.stt = TranscriptionEngine()
        self.running = False
        self.hotkeys = HotkeyManager(self)
    def run(self):
        logger.info("WhisperCast ready. Use hotkeys to control. Press Ctrl+C or hotkey to quit.")
        self.hotkeys.start()
        try:
            self._loop()
        except KeyboardInterrupt:
            logger.info("Exiting…")
            self.audio.stop()
    def _loop(self):
        buffer = b""
        buffer_duration = 0.0
        CHUNK_DURATION = 0.03
        BUFFER_LIMIT = 10.0  # Adjustable for sentence length
        
        while True:
            if not self.running:
                if buffer:
                    self._process_buffer(buffer)
                buffer = b""
                buffer_duration = 0.0
                sleep(0.1)
                continue
            pcm = self.audio.read(timeout=0.1)
            if not pcm:
                continue
            buffer += pcm
            buffer_duration += CHUNK_DURATION
            
            if buffer_duration >= BUFFER_LIMIT:
                self._process_buffer(buffer)
                buffer = b""
                buffer_duration = 0.0

    def _process_buffer(self, buffer):
        raw = self.stt.transcribe(buffer)
        if raw.strip():
            print("\nTranscribed:", raw)
        else:
            logger.info("Empty transcription skipped")

    def toggle_recording(self):
        if self.running:
            self.audio.stop()
            self.running = False
            print("\n Recording stopped.")
            logger.info("Recording paused")
        else:
            self.audio.start()
            self.running = True
            print("\n Recording started! Speak now...")
            logger.info("Recording started")

if __name__ == "__main__":
    WhisperCastApp().run()
