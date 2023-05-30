import pygame
import random
import theGame
import Equipment
import Wearable
import Creature
import specialActions
import tkinter as tk
from pygame.locals import *
from tkinter import simpledialog

def play_final():
    level = theGame.theGame()._level
    if event.type == KEYDOWN :
        num=pygame.key.name(event.key)
        if num in theGame.theGame()._actions:
            theGame.theGame()._actions[num](theGame.theGame()._hero)
    if theGame.theGame()._level != level:
        screen2.fill("white")
    theGame.theGame()._hero.checkPoison()
    theGame.theGame()._floor.moveAllMonsters()
        

def textInput(titre, message):
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale

    # Boîte de dialogue pour saisir du texte
    user_input = simpledialog.askstring(titre, message)

    # Afficher le texte saisi
    if user_input:
        return user_input
def update_health(surface):
    percent = 230 * (theGame.theGame().getHero().getHP() / theGame.theGame().getHero().hpMax)
    bar_position=[surface.get_width()-290,15,percent,60]
    back_bar_position=[surface.get_width()-290,15,230,60]
    pygame.draw.rect(surface,(80, 88, 94),back_bar_position)
    pygame.draw.rect(surface,("green"),bar_position)
    
pygame.init()
running = True
game = False
aide = False
flags = pygame.FULLSCREEN | pygame.RESIZABLE
clock = pygame.time.Clock()
pygame.display.set_caption("DONGEON MASTER")
res = (1440, 810)
screen = pygame.display.set_mode(res, pygame.RESIZABLE)
sol = pygame.transform.scale(pygame.image.load("assets/sol.png").convert(), (66, 66))
mur1 = pygame.transform.scale(pygame.image.load("assets/mur1.png").convert(), (66, 66))
mur2 = pygame.transform.scale(pygame.image.load("assets/mur2.png").convert(), (66, 66))

equipments = {
        0: [
            Equipment.Equipment("potion", "p", usage=lambda self, hero: specialActions.heal(hero)),
            Wearable.Wearable(
                "broken sword", place="right hand", effect={"strength": 1}, usage=lambda self, hero: specialActions.equip(hero, self)
            ),
            Wearable.Wearable(
                "trident", place="right hand", effect={"strength": 3}, usage=lambda self, hero: specialActions.equip(hero, self)
            ),
            Wearable.Wearable(
                "double_epee", place="right hand", effect={"strength": 2}, usage=lambda self, hero: specialActions.equip(hero, self)
            ),
            Equipment.Equipment("gold", "o"),
        ],
        1: [Equipment.Equipment("potion de tp", "!", usage=lambda self, hero: specialActions.teleport(hero, True))],
        2: [
            Wearable.Wearable(
                "sword", place="right hand", effect={"strength": 2}, usage=lambda self, hero: specialActions.equip(hero, self)
            ),
            Equipment.Equipment("bow"),
            Wearable.Wearable("leather vest", place="torso", effect={"armor": 1}),
            Equipment.Equipment("antidotal", usage=lambda self, hero: specialActions.recover(hero, True)),
        ],
        3: [
            Equipment.Equipment("portoloin", "w", usage=lambda self, hero: specialActions.teleport(hero, False)),
            Equipment.Equipment("invisibility potion", "i", usage=lambda self, hero: hero.becomeInvisible()),
        ],
        4: [Wearable.Wearable("chainmail", place="torso", effect={"armor": 2})],
    }

dict_sol ={
        "G": pygame.transform.scale(pygame.image.load("assets/sol/goblinsol.png").convert(), (66, 66)),
        "E":pygame.transform.scale(pygame.image.load("assets/sol/escalier_sol.png").convert(), (66, 66)),
        "W":pygame.transform.scale(pygame.image.load("assets/sol/bat_sol.png").convert(), (66, 66)),
        "O": pygame.transform.scale(pygame.image.load("assets/sol/orksol.png").convert(), (66, 66)),
        "B":pygame.transform.scale(pygame.image.load("assets/sol/blobsol.png").convert(), (66, 66)),
        "S":pygame.transform.scale(pygame.image.load("assets/sol/spider_sol.png").convert(), (66, 66)),
        "D":pygame.transform.scale(pygame.image.load("assets/sol/dragonsol.png").convert(), (66, 66)),
        "p":pygame.transform.scale(pygame.image.load("assets/sol/potion_hp_sol.png").convert(), (66, 66)),
        "n":pygame.transform.scale(pygame.image.load("assets/sol/brokensword_sol.png").convert(), (66, 66)),
        "t":pygame.transform.scale(pygame.image.load("assets/sol/trident_sol.png").convert(), (66, 66)),
        "d":pygame.transform.scale(pygame.image.load("assets/sol/double_epee_sol.png").convert(), (66, 66)),
        "o":pygame.transform.scale(pygame.image.load("assets/sol/gold_sol.png").convert(), (66, 66)),
        "!":pygame.transform.scale(pygame.image.load("assets/sol/teleport_potion_sol.png").convert(), (66, 66)),
        "s":pygame.transform.scale(pygame.image.load("assets/sol/epeesol.png").convert(), (66, 66)),
        "b":pygame.transform.scale(pygame.image.load("assets/sol/arcsol.png").convert(), (66, 66)),
        "l":pygame.transform.scale(pygame.image.load("assets/sol/leathervestsol.png").convert(), (66, 66)),
        "a":pygame.transform.scale(pygame.image.load("assets/sol/antidote_sol.png").convert(), (66, 66)),
        "w":pygame.transform.scale(pygame.image.load("assets/sol/portoloin_sol.png").convert(), (66, 66)),
        "i":pygame.transform.scale(pygame.image.load("assets/sol/invisibility_potion_sol.png").convert(), (66, 66)),
        "c":pygame.transform.scale(pygame.image.load("assets/sol/chainmail_sol.png").convert(), (66, 66)),
        "@":pygame.transform.scale(pygame.image.load("assets/sol/herosol.png").convert(), (66, 66)),
        "e":pygame.transform.scale(pygame.image.load("assets/sol/shopsol.png").convert(), (66, 66)),
        "M":pygame.transform.scale(pygame.image.load("assets/sol/coffre_ferme_sol.png").convert(), (66, 66)),
        "Mo":pygame.transform.scale(pygame.image.load("assets/sol/coffre_ouvert_sol.png").convert(), (66, 66))
        }

while running:
    scrrec = screen.get_rect()
    background = pygame.transform.scale(pygame.image.load("assets/background lancement.png").convert(), (scrrec.right, scrrec.bottom))
    screen.blit(background, (0, 0))
    play_button = pygame.image.load("assets/LOGO-PLAY.png")
    play_button_rect = play_button.get_rect()
    play_button_rect.center = screen.get_rect().center
    screen.blit(play_button, play_button_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            running = False
        elif event.type == KEYDOWN and event.key == K_h:
            screen_aide = pygame.display.set_mode((0,0), flags)
            aide = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                screen2 = pygame.display.set_mode((0, 0), flags)
                screen2.fill("white")
                theGame.theGame().buildFloor()
                for i in range(13):
                    for j in range(13):
                        if theGame.theGame()._floor._mat[j][i] == theGame.theGame()._floor.empty:
                            if random.randint(0, 1) == 0:
                                screen2.blit(mur1,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
                            else:
                                screen2.blit(mur2,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
                        elif theGame.theGame()._floor._mat[j][i] == theGame.theGame()._floor.ground:
                            text = "#theGame.theGame()._floor._mat[j][i]==theGame.theGame()._floor.ground or a ==1 :"
                            screen2.blit(sol,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
                        elif  theGame.theGame()._floor._mat[j][i]!=theGame.theGame()._floor.empty:
                            elem=theGame.theGame()._floor._mat[j][i]
                            if not isinstance(theGame.theGame()._floor._mat[j][i],str):
                                elem=elem.get_abbrv()
                            screen2.blit(dict_sol[elem],((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)

                running = False
                game = True

    while aide:
        scrrec_aide = screen_aide.get_rect()
        screen_aide.fill([255, 255, 255])
        background = pygame.transform.scale(pygame.image.load("assets/help.png").convert(), (scrrec_aide.right, scrrec_aide.bottom))
        screen_aide.blit(background, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                aide = False
                screen = pygame.display.set_mode(res, pygame.RESIZABLE)
                screen = pygame.display.set_mode(res, pygame.RESIZABLE)
                background = pygame.transform.scale(pygame.image.load("assets/background lancement.png").convert(), (scrrec.right, scrrec.bottom))
                screen.blit(background, (0, 0))
                running = True

    while game and theGame.theGame().getHero().getHP() > 0:
        varText = "Press ESCAPE to quit"
        font = pygame.font.Font("freesansbold.ttf", 40)
        text = font.render(varText, True, "black")
        textRect = text.get_rect()
        textRect.center = (210, screen2.get_size()[1] - 25)
        screen2.blit(text, textRect)
        update_health(screen2)
        for event in pygame.event.get():
            if event.type !=KEYDOWN :
                continue 
            play_final()
            if event.type == KEYDOWN and event.key == K_k:
                pygame.display.set_mode(res, pygame.RESIZABLE)
                pygame.display.set_mode(res, pygame.RESIZABLE)
                game = False
                running = True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game = False
                running = False
            for i in range(13):
                    for j in range(13):
                        if theGame.theGame()._floor._mat[j][i] == theGame.theGame()._floor.ground:
                            text = "#theGame.theGame()._floor._mat[j][i]==theGame.theGame()._floor.ground or a ==1 :"
                            screen2.blit(sol,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
                        elif theGame.theGame()._floor._mat[j][i] == theGame.theGame()._floor.empty:
                            screen2.blit(mur1,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
                        elif  theGame.theGame()._floor._mat[j][i]!=theGame.theGame()._floor.empty:
                            elem=theGame.theGame()._floor._mat[j][i]
                            if not isinstance(theGame.theGame()._floor._mat[j][i],str):
                                elem=elem.get_abbrv()
                            screen2.blit(dict_sol[elem],((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
        pygame.display.update()
    print('Game OVER')

