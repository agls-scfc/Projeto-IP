import pygame 

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y