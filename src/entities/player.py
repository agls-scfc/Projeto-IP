import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        # placeholder visual
        self.image = pygame.Surface((32, 48))
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
