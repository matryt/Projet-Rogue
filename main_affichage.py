import pygame
import os
import math
from pygame.locals import *
pygame.init()
running = True
game = False
aide = False
flags= pygame.FULLSCREEN | pygame.RESIZABLE
clock = pygame.time.Clock()
pygame.display.set_caption("DONGEON MASTER")
if os.name=="posix":
    res=(1820,980)
elif os.name=='nt':
    res=(1440,810)
screen=pygame.display.set_mode(res,pygame.RESIZABLE)
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
                running=False
                screen2 = pygame.display.set_mode((0,0),flags)
                game = True

    while aide :
        screen_aide.fill('red')
        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                aide=False
                screen=pygame.display.set_mode(res,pygame.RESIZABLE)
                running=True

    while game :
        screen2.fill('white')
        varText = "Press ESCAPE to quit"
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render(varText, True, 'black')
        textRect = text.get_rect()
        textRect.center = (210,screen2.get_size()[1]-25)
        screen2.blit(text, textRect)
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
            
