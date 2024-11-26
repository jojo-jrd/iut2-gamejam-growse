# -- Initialisation --

# STL

# PyGames
import pygame
from pygame.locals import *

# Personnels
from src.element import Element
from src.window  import Window
from src.text    import Text
from src.button  import Button
from src.image   import Image
from src.terrain import Terrain

from src.pages   import *

pygame.init()
pygame.font.init()

# Rules

# -- Création des objets --

# Fenêtre
window = Window((1024, 768))

init_pages(window)
init_accueil(window)
init_difficulte(window)
init_credits(window)
init_jeu(window)
init_control_jeu(window)
init_regles1(window)
init_regles2(window)
init_control(window)
init_defaite(window)
init_victoire(window)
init_echap(window)

# -- Boucle principale --
window.runSound("src/musics/musique/menu.mp3")

while window.active:
    # Event's managment
    for event in pygame.event.get():
        window.checkEvent(window, event)

    # Refresh
    window.update()
    window.refresh()
