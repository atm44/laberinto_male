# Standard library imports
import asyncio
import os

# Local folder imports
from game import Game

if __name__ == "__main__":
    
    img_folder = os.path.join( "images")
    snd_folder = os.path.join( "snd")
    game = Game(snd_folder = snd_folder,img_folder = img_folder)
    asyncio.run(game.run())
