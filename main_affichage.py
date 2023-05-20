import pygame
from pygame.locals import *
pygame.init()
running = True
game = False
clock = pygame.time.Clock()
while running:
    pygame.display.set_caption("DONGEON MASTER")
    fenetre = pygame.display.set_mode((0, 0), (pygame.RESIZABLE))
    fenetre.convert()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            running = False
        if event.type==pygame.quit():
            pygame.quit()
            running = False
