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
    varText = "Press ESCAPE to quit"
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render(varText, True, 'black')
    textRect = text.get_rect()
    textRect.center = (210,fenetre.get_size()[1]-25)
    fenetre.blit(text, textRect)
    pygame.display.flip()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            running = False
