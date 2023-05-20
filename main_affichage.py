import pygame
from pygame.locals import *
pygame.init()

running = True
game = False

clock = pygame.time.Clock()
pygame.display.set_caption("DONGEON MASTER")
fenetre = pygame.display.set_mode((0, 0), (pygame.RESIZABLE))
while running:
    fenetre.fill([0,0,128])
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            running = False
