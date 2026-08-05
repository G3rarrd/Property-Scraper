from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
SESSION_DIR = PROJECT_ROOT / "sessions"

for directory in (DATA_DIR, LOG_DIR, SESSION_DIR):
    directory.mkdir(parents=True, exist_ok=True)