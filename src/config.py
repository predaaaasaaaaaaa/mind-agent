from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
TRIBEV2_CACHE = "/home/preda/tribev2-cache"
N_VOXELS = 20484
TR_SECONDS = 1  # one prediction per second
DEFAULT_VIDEO_PATH = "/home/preda/Downloads/test_short.mp4"

OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)
