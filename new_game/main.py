# Standard library imports
import os
import sys
import logging

# Local folder imports
from game import Game

# logging setup: write debug.log next to this script
script_dir = os.path.dirname(__file__)
log_path = os.path.join(script_dir, "debug.log")
logging.basicConfig(level=logging.DEBUG, filename=log_path, filemode='w',
                    format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
# also log to console so messages appear when running in terminal
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
logger.addHandler(console_handler)

if __name__ == "__main__":
    try:
        img_folder = os.path.join("images")
        snd_folder = os.path.join("snd")
        logger.debug("Starting game (main)")
        logger.debug(f"img_folder={img_folder}, snd_folder={snd_folder}")
        game = Game(snd_folder=snd_folder, img_folder=img_folder)
        game.run()
    except Exception:
        logger.exception("Unhandled exception running game")
        raise
