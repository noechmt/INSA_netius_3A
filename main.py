from GUI.title_screen import title_screen
import p2p.connect as p2p
import pygame
import sys
import os
import ctypes

# Check of the version of python, 3.10 or 3.11
assert sys.version[0:4] == "3.10" or sys.version[0:
                                                 4] == "3.11", "Merci d'utiliser une version de python >= 3.10 !"

# Check if all the dependencies are installed
os.system(str(sys.executable) + " -m pip install -r requirements.txt")

if os.name == "nt":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


if __name__ == "__main__":
    p2p.socket_init()
    if (title_screen()):
        from game_screen.game_screen import game_screen
        game_screen()
    pygame.quit()
