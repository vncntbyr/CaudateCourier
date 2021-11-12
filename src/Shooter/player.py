import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('./images/playerModel.png')
        self.rect = self.image.get_rect(midbottom = pos)
        