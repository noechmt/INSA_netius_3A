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

# Delete the lan_conne process if it exists
os.system("pgrep -f lan_conne | xargs kill -9")
os.system("make clean -C p2p")
os.system("make -C p2p")

if __name__ == "__main__":
    retour = title_screen()
    if (retour[0]):
        from game_screen.game_screen import game_screen
        game_screen(retour[1])
    pygame.quit()

# TO-DO
# Play Blackjack with nearby governor
