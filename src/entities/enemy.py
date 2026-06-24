import pygame
class Enemy:
    def __init__(self, x ,y):
        self.x=x
        self.y=y
        self.width=40
        self.height=40
        self.speed=2
        self.image= pygame.image.load("Projeto-IP/src/images/inimigo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_original = self.image

    def update(self):
        self.x += self.speed
        if self.x > 800 - self.width:
            self.speed = -2
            self.image = pygame.transform.flip(self.image_original, True, False)
        if self.x < 0:
            self.speed = 2
            self.image = self.image_original

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        

