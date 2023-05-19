import pygame
import math
from pygame.locals import *
pygame.init()

running = True 
game = False

    
    
clock = pygame.time.Clock()
while running :
    pygame.display.set_caption("Calcul mental ")
    fenetre = pygame.display.set_mode((0,0), (pygame.RESIZABLE))
    fenetre.convert()
    pygame.display.update()

    pygame.display.update()
    for event in pygame.event.get():
        if event.type ==KEYDOWN:
            if event.key==K_ESCAPE:
                pygame.quit()
                running= False
                
                
            

