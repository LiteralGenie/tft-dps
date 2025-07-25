from pathlib import Path

SRC_DIR = Path(__file__).parent.parent

DATA_DIR = SRC_DIR.parent / "data"

TFT_DB_FILE = DATA_DIR / "tft.sqlite"

for fp in [
    DATA_DIR,
]:
    fp.mkdir(exist_ok=True, parents=True)
