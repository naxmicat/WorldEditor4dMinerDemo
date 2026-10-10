import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GAME_PATH = Path(os.environ.get('GAME_PATH'))
WORLDS_PATH = GAME_PATH / "worlds"
