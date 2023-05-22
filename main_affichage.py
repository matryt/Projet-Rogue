import pygame
import math
from pygame.locals import *
pygame.init()

running = True
game = False

clock = pygame.time.Clock()
pygame.display.set_caption("DONGEON MASTER")
screen= pygame.display.set_mode((0, 0),FULLSCREEN)
screen2 = pygame.display.set_mode((0, 0),FULLSCREEN)
while running:
    screen.fill([0,0,128])
    varText = "Press ESCAPE to quit"
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render(varText, True, 'black')
    textRect = text.get_rect()
    textRect.center = (210,screen.get_size()[1]-25)
    screen.blit(text, textRect)
    play_button = pygame.image.load('assets/bouton.png')
    play_button_rect = play_button.get_rect()
    play_button_rect.center=screen.get_rect().center
    screen.blit(play_button,play_button_rect)
    pygame.display.flip()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type ==pygame.QUIT :
                running= False
                pygame.quit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN :
            if play_button_rect.collidepoint(event.pos) :
                running=False
                game = True
                
    
    while game :
        screen2.fill([0,0,128])
        varText = ""
        textRect = text.get_rect()
        textRect.center = (210,screen2.get_size()[1]-25)
        screen2.blit(text, textRect)
        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type ==pygame.QUIT :
                running= False
                game = False
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                running = False
            
            



