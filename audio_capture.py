import pyaudio
import queue
from .utils import load_config, logger
class AudioCapture:
    def __init__(self):
        cfg = load_config()["audio"]
        self.rate = cfg["sample_rate"]
        self.chunk = cfg["chunk_size"]
        self._queue = queue.Queue()
        self.p = pyaudio.PyAudio()
        self.stream = None
    def start(self):
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self._callback,
        )
        self.stream.start_stream()
        logger.info("Audio capture started")
    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        logger.info("Audio capture stopped")
    def read(self, timeout=0.1):
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None
    def _callback(self, in_data, *_):
        self._queue.put(in_data)
        return (in_data, pyaudio.paContinue)

