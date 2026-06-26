import pygame
class Player:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 2
        self.image = pygame.image.load("Projeto-IP/src/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_original = self.image
        self.velocidade_y = 0
        self.no_chao = True

    def update(self):
        teclas=pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.x -= self.speed
            self.image = pygame.transform.flip(self.image_original, True, False)
        if teclas[pygame.K_RIGHT]:
            self.x +=self.speed
            self.image = self.image_original
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = -10
            self.no_chao = False

        self.velocidade_y +=0.5
        self.y += self.velocidade_y

        if self.y >= 500:
            self.y = 500
            self.velocidade_y = 0
            self.no_chao = True
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

