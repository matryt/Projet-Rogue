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
    white = (255, 255, 255) 
    green = (0, 255, 0) 
    blue = (0, 0, 128) 
    varText = ""
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render(varText, True, green,blue)
    textRect = text.get_rect()
    textRect.center = (960, 540)
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            running = False
