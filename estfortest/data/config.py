import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, 'abis')

GAME_ABI = os.path.join(ABIS_DIR, 'Game.json')
PLAYER_ABI = os.path.join(ABIS_DIR, 'players.json')

ftm_rpc = 'https://fantom-rpc.publicnode.com'

private_key = ''