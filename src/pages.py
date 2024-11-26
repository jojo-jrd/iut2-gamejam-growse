# -- Initialisation --

# STL

# PyGames
import pygame
from pygame.locals import *

# Personnels
from src.element         import Element
from src.animate_element import AnimateElement
from src.window          import Window
from src.text            import Text
from src.button          import Button
from src.image           import Image
from src.terrain         import Terrain
from src.inventaire import Inventaire
from src.joueur import Joueur
from src.soldat import Soldat
from src.boutique import Boutique

# -- Callbacks --

def lunch_game(window):
    window.removeMode('jeu')

    global terrain
    terrain = Terrain((0,0))

    control_button = Button((3,2), lunch_control_game)
    control_button.loadBackground('src/images/Accueil/fr-control_button.png', (-1,-1), 'fr')
    control_button.loadBackground('src/images/Accueil/en-control_button.png', (-1,-1), 'en')
    control_button.size = (150,-1)

    window.addSprite('jeu', terrain)

    window.addSprite('jeu', control_button)

def lunch_difficulte(window):
    window.current_mode = 'difficulte'

def lunch_credits(window):
    window.current_mode = 'credits'

def lunch_game_easy(window):
    lunch_game(window)
    terrain.initialisation(window, 1,1)
    window.stopSound()
    window.runSound("src/musics/musique/journee.mp3")
    window.current_mode = 'jeu'

def lunch_game_meduim(window):
    lunch_game(window)
    terrain.initialisation(window, 1,2)
    window.stopSound()
    window.runSound("src/musics/musique/journee.mp3")
    window.current_mode = 'jeu'

def lunch_game_difficult(window):
    lunch_game(window)
    terrain.initialisation(window, 1,3)
    window.stopSound()
    window.runSound("src/musics/musique/journee.mp3")
    window.current_mode = 'jeu'

def lunch_game_accueil(window):
    window.current_mode = 'accueil'

def lunch_game_accueil_musique(window):
    window.stopSound()
    window.runSound("src/musics/musique/menu.mp3")
    window.current_mode = 'accueil'


def lunch_control_game(window):
    window.current_mode = 'controlesJeu'

def lunch_game_retour_control(window):
    window.current_mode = 'jeu'

def lunch_echap(window):
    window.current_mode = 'echap'

def lunch_game_victoire(window):
    window.current_mode = 'victoire'

def lunch_game_defaite(window):
    window.current_mode = 'defaite'

def lunch_regles1(window):
    window.current_mode = 'regles1'

def lunch_regles2(window):
    window.current_mode = 'regles2'

def lunch_control(window):
    window.current_mode = 'controles'

def lunch_anglais(window):
    window.langue = 'en'
    window.current_mode = 'accueil'

def lunch_francais(window):
    window.langue = 'fr'
    window.current_mode = 'accueil'

# -- Globals --

def init_pages(window):
    global credits_button
    credits_button = Button((1024 - 16, 768 - 74), lunch_credits)
    credits_button.loadBackground('src/images/Accueil/credits_button.png')
    credits_button.alignment = 'top-right'


# -- Accueil --

def init_accueil(window):
    name = Image((1024 / 2, 100),"src/images/Accueil/nom.png")
    name.alignment = 'top-center'

    game_button = Button((1024 / 2, 350), lunch_difficulte)
    rules_button = Button((1024 / 2, 2/3 * 768), lunch_regles1)
    control_button = Button((1024 / 2, 2/3 * 768 + 140), lunch_control)

    game_button.loadBackground('src/images/Accueil/fr-play_button.png', (-1,-1), 'fr')
    rules_button.loadBackground('src/images/Accueil/fr-rules_button.png', (-1,-1), 'fr')
    control_button.loadBackground('src/images/Accueil/fr-control_button.png', (-1,-1), 'fr')
    game_button.loadBackground('src/images/Accueil/en-play_button.png', (-1,-1), 'en')
    rules_button.loadBackground('src/images/Accueil/en-rules_button.png', (-1,-1), 'en')
    control_button.loadBackground('src/images/Accueil/en-control_button.png', (-1,-1), 'en')


    rules_button.alignment = 'middle'
    rules_button.size = (400,-1)

    game_button.alignment = 'middle'
    game_button.size = (300,-1)

    control_button.alignment = 'middle'
    control_button.size = (300,-1)

    francais_button = Button((1024-1000,768 - 74), lunch_francais)
    francais_button.loadBackground('src/images/Accueil/langue-fr.png')
    francais_button.alignment = 'left'

    english_button = Button((1024-900,768 - 74), lunch_anglais)
    english_button.loadBackground('src/images/Accueil/langue-en.png')
    english_button.alignment = 'left'

    window.addSprite('accueil', Image((0,0), "src/images/Accueil/bg_accueil.png", (1024, -1)))
    window.addSprite('accueil', name)
    window.addSprite('accueil', game_button)
    window.addSprite('accueil', control_button)
    window.addSprite('accueil', rules_button)
    window.addSprite('accueil', francais_button)
    window.addSprite('accueil', english_button)
    window.addSprite('accueil', credits_button)


# -- Difficulté --

def init_difficulte(window):
    easy_button = Button((1024 / 2, 1/3 * 768), lunch_game_easy)
    medium_button = Button((1024 / 2, 1/2 * 768), lunch_game_meduim)
    return_button = Button((3,2), lunch_game_accueil)
    difficult_button = Button((1024 / 2, 2/3 * 768), lunch_game_difficult)

    easy_button.loadBackground('src/images/Accueil/fr-easy_button.png', (-1,-1), 'fr')
    medium_button.loadBackground('src/images/Accueil/fr-medium_button.png', (-1,-1), 'fr')
    difficult_button.loadBackground('src/images/Accueil/fr-difficult_button.png', (-1,-1), 'fr')
    easy_button.loadBackground('src/images/Accueil/en-easy_button.png', (-1,-1), 'en')
    medium_button.loadBackground('src/images/Accueil/en-medium_button.png', (-1,-1), 'en')
    difficult_button.loadBackground('src/images/Accueil/en-difficult_button.png', (-1,-1), 'en')


    return_button.loadBackground('src/images/Accueil/return_button.png')

    return_button.alignment = 'left'
    easy_button.alignment = 'middle'
    medium_button.alignment = 'middle'
    difficult_button.alignment = 'middle'
    easy_button.size = (200,-1)
    medium_button.size = (250,-1)
    difficult_button.size = (250,-1)

    window.addSprite('difficulte', Image((0,0), "src/images/Accueil/bg_accueil.png", (1024,-1)))
    window.addSprite('difficulte', easy_button)
    window.addSprite('difficulte', medium_button)
    window.addSprite('difficulte', difficult_button)
    window.addSprite('difficulte', return_button)
    window.addSprite('difficulte', credits_button)

# -- Crédits --

def init_credits(window):
    return_button = Button((3,2), lunch_game_accueil)
    return_button.loadBackground('src/images/Accueil/return_button.png')
    return_button.alignment = 'left'


    window.addSprite('credits', Image((0,0), "src/images/Accueil/fr-credit.png", (1024,-1), 'fr'))
    window.addSprite('credits', Image((0,0), "src/images/Accueil/en-credit.png", (1024,-1), 'en'))


    window.addSprite('credits', return_button)

# -- Règles --

def init_regles1(window):
    return_button = Button((3,2), lunch_game_accueil)
    return_button.loadBackground('src/images/Accueil/return_button.png')
    return_button.alignment = 'left'

    regle_button2 = Button((1024-3,768/2), lunch_regles2)
    regle_button2.loadBackground('src/images/Accueil/page2_button.png')
    regle_button2.alignment = 'top-right'

    window.addSprite('regles1', Image((0,0), "src/images/Accueil/fr-rule-1.png", (1024,-1), 'fr'))
    window.addSprite('regles1', Image((0,0), "src/images/Accueil/en-rule-1.png", (1024,-1), 'en'))

    window.addSprite('regles1', regle_button2)
    window.addSprite('regles1', return_button)

def init_regles2(window):
    return_button = Button((3,2), lunch_game_accueil)
    return_button.loadBackground('src/images/Accueil/return_button.png')
    return_button.alignment = 'left'

    regle_button1 = Button((3,768/2), lunch_regles1)
    regle_button1.loadBackground('src/images/Accueil/return_button.png')
    regle_button1.alignment = 'left'


    window.addSprite('regles2', Image((0,0), "src/images/Accueil/fr-rule-2.png", (1024,-1), 'fr'))
    window.addSprite('regles2', Image((0,0), "src/images/Accueil/en-rule-2.png", (1024,-1), 'en'))

    window.addSprite('regles2', regle_button1)
    window.addSprite('regles2', return_button)

# -- Controles --

def init_control(window):
    return_button = Button((3,2), lunch_game_accueil)
    return_button.loadBackground('src/images/Accueil/return_button.png')
    return_button.alignment = 'left'


    window.addSprite('controles', Image((0,0), "src/images/Accueil/fr-control.png", (1024,-1),'fr'))
    window.addSprite('controles', Image((0,0), "src/images/Accueil/en-control.png", (1024,-1),'en'))

    window.addSprite('controles', return_button)

def init_control_jeu(window):
    return_button = Button((3,2), lunch_game_retour_control)
    return_button.loadBackground('src/images/Accueil/return_button.png')
    return_button.alignment = 'left'


    window.addSprite('controlesJeu', Image((0,0), "src/images/Accueil/fr-control.png", (1024,-1),'fr'))
    window.addSprite('controlesJeu', Image((0,0), "src/images/Accueil/en-control.png", (1024,-1),'en'))

    window.addSprite('controlesJeu', return_button)

# -- Jeu --

def init_jeu(window):
    pass

def init_victoire(window):
    return_button = Button((3,2), lunch_game_accueil)
    return_button.loadBackground('src/images/Accueil/return_button.png')
    return_button.alignment = 'left'
    
    try_button = Button((1024 / 2, 768*3/4 ), lunch_difficulte)
    try_button.loadBackground('src/images/Accueil/fr-try-again.png', (-1,-1), 'fr')
    try_button.loadBackground('src/images/Accueil/en-try-again.png', (-1,-1), 'en')
    try_button.alignment = 'middle'

    window.addSprite('victoire', Image((0,0), "src/images/Accueil/fr-win.png", (1024,-1),'fr'))
    window.addSprite('victoire', Image((0,0), "src/images/Accueil/en-win.png", (1024,-1),'en'))

    window.addSprite('victoire', return_button)
    window.addSprite('victoire', try_button)



def init_defaite(window):
    return_button = Button((3,2), lunch_game_accueil)
    return_button.loadBackground('src/images/Accueil/return_button.png')
    return_button.alignment = 'left'

    try_button = Button((1024 / 2, 768*3/4 ), lunch_difficulte)
    try_button.loadBackground('src/images/Accueil/fr-try-again.png', (-1,-1), 'fr')
    try_button.loadBackground('src/images/Accueil/en-try-again.png', (-1,-1), 'en')
    try_button.alignment = 'middle'


    window.addSprite('defaite', Image((0,0), "src/images/Accueil/fr-game-over.png", (1024,-1),'fr'))
    window.addSprite('defaite', Image((0,0), "src/images/Accueil/en-game-over.png", (1024,-1),'en'))

    window.addSprite('defaite', return_button)
    window.addSprite('defaite', try_button)

def init_echap(window):
    echap = Image((1024 / 2,768/2), "src/images/Accueil/fr-quit.png", (-1,-1),'fr')
    echap.loadBackground("src/images/Accueil/en-quit.png", (-1,-1), 'en')
    echap.alignment ='middle'
    echap.size = (1024/2,-1)
    window.addSprite('echap', echap)

    oui_button = Button((1024 / 2-100, 768*1/2 +20), lunch_game_accueil_musique) # A tester si le jeu continue au pas
    oui_button.loadBackground('src/images/Accueil/fr-yes.png', (-1,-1), 'fr')
    oui_button.loadBackground('src/images/Accueil/en-yes.png', (-1,-1), 'en')
    oui_button.alignment = 'middle'

    non_button = Button((1024 / 2+100, 768*1/2 +20 ), lunch_game_retour_control)
    non_button.loadBackground('src/images/Accueil/fr-no.png', (-1,-1), 'fr')
    non_button.loadBackground('src/images/Accueil/en-no.png', (-1,-1), 'en')
    non_button.alignment = 'middle'

    window.addSprite('echap', oui_button )
    window.addSprite('echap', non_button )
