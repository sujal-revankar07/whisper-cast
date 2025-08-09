import logging
import toml
from pathlib import Path
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "config.toml"
def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    return toml.load(CONFIG_PATH)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("WhisperCast")
