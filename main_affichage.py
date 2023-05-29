import pygame
import random
import theGame
import tkinter as tk
from pygame.locals import *
from tkinter import simpledialog

def textInput(titre, message):
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale

    # Boîte de dialogue pour saisir du texte
    user_input = simpledialog.askstring(titre, message)

    # Afficher le texte saisi
    if user_input:
        return user_input

pygame.init()
running = True
game = False
aide = False
flags= pygame.FULLSCREEN | pygame.RESIZABLE
clock = pygame.time.Clock()
pygame.display.set_caption("DONGEON MASTER")
res=(1440,810)
screen=pygame.display.set_mode(res,pygame.RESIZABLE)
sol=pygame.transform.scale(pygame.image.load('assets/sol.png').convert(),(70,70))
mur1=pygame.transform.scale(pygame.image.load('assets/mur1.png').convert(),(70,70))
mur2=pygame.transform.scale(pygame.image.load('assets/mur2.png').convert(),(70,70))

while running:
    scrrec=screen.get_rect()
    background=pygame.transform.scale(pygame.image.load('assets/background lancement.png').convert(),(scrrec.right,scrrec.bottom))
    screen.blit(background,(0,0))
    play_button = pygame.image.load('assets/LOGO-PLAY.png')
    play_button_rect = play_button.get_rect()
    play_button_rect.center=screen.get_rect().center
    screen.blit(play_button,play_button_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type ==pygame.QUIT :
            running= False
            pygame.quit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            running = False
        elif event.type == KEYDOWN and event.key == K_h :
            screen_aide=pygame.display.set_mode((res[0]*(9/10),res[1]*(9/10)))
            aide=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos) :
                screen2 = pygame.display.set_mode((0,0),flags)
                screen2.fill('white')
                theGame.theGame().buildFloor()
                print(theGame.theGame()._floor)
                a=1
                for i in range(13):
                    for j in range(13):
                        if theGame.theGame()._floor._mat[j][i]==theGame.theGame()._floor.empty:
                            if random.randint(0,1)==0:
                                screen2.blit(mur1,((screen2.get_width()-13*70)/2+i*70,(screen2.get_height()-13*70)/2+j*70))
                            else :
                                screen2.blit(mur2,((screen2.get_width()-13*70)/2+i*70,(screen2.get_height()-13*70)/2+j*70))
                        else : 
                            text="#theGame.theGame()._floor._mat[j][i]==theGame.theGame()._floor.ground or a ==1 :"
                            screen2.blit(sol,((screen2.get_width()-13*70)/2+i*70,(screen2.get_height()-13*70)/2+j*70))
                running=False
                game = True
    
    while aide :
        screen_aide.fill('white')
        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                aide=False
                screen=pygame.display.set_mode(res,pygame.RESIZABLE)
                running=True
    
    while game :
        varText = "Press ESCAPE to quit"
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render(varText, True, 'black')
        textRect = text.get_rect()
        textRect.center = (210,screen2.get_size()[1]-25)
        screen2.blit(text, textRect)
        for i in range(13):
            for j in range(13):
                if theGame.theGame()._floor._mat[j][i]==theGame.theGame()._floor.ground :
                    screen2.blit(sol,((screen2.get_width()-13*70)/2+i*70,(screen2.get_height()-13*70)/2+j*70))
                        

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_k:
                pygame.display.set_mode(res,pygame.RESIZABLE)
                pygame.display.set_mode(res,pygame.RESIZABLE)
                game=False
                running=True
            if event.type == KEYDOWN and event.key == K_ESCAPE :
                game=False
                running = False
            
