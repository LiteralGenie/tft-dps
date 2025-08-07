from pathlib import Path

SRC_DIR = Path(__file__).parent.parent

DATA_DIR = SRC_DIR.parent / "data"
LOG_DIR = DATA_DIR / "logs"
CD_DIR = DATA_DIR / "cdragon"
DEBUG_DIR = DATA_DIR / "debug"

TFT_DB_FILE = DATA_DIR / "tft.sqlite"

for fp in [
    DATA_DIR,
    LOG_DIR,
    CD_DIR,
]:
    fp.mkdir(exist_ok=True, parents=True)
