import numpy as np
import importlib.util
from faster_whisper import WhisperModel
from .utils import load_config, logger
class TranscriptionEngine:
    def __init__(self):
        cfg = load_config()["transcription"]
        device = cfg["device"]
        compute_type = cfg["compute_type"]        
        if device == "auto":
            torch_spec = importlib.util.find_spec("torch")
            if torch_spec is not None:
                torch = importlib.util.module_from_spec(torch_spec)
                torch_spec.loader.exec_module(torch)
                if torch.cuda.is_available():
                    device = "cuda"
                    compute_type = "float16"
                    logger.info("GPU detected - Using CUDA")
                else:
                    device = "cpu"
                    logger.info("No GPU detected - Falling back to CPU")
            else:
                device = "cpu"
                logger.warning("Torch not installed - Using CPU")        
        self.model = WhisperModel(
            cfg["model_size"],
            device=device,
            compute_type=compute_type,
        )
        self.rate = load_config()["audio"]["sample_rate"]
    def transcribe(self, pcm_bytes: bytes) -> str:
        audio = np.frombuffer(pcm_bytes, np.int16).astype(np.float32) / 32768.0
        segments, _ = self.model.transcribe(audio, beam_size=1, language="en")
        segments_list = list(segments)
        text = " ".join([s.text.strip() for s in segments_list])
        return text
