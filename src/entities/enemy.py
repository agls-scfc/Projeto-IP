import pygame
class Enemy:
    def __init__(self, x ,y):
        self.x=x
        self.y=y
        self.width=40
        self.height=40
        self.speed=1.4
        self.spritesheet = pygame.image.load("src/images/inimigosprites.png").convert_alpha()
        self.frame_largura = self.spritesheet.get_width() // 3
        self.frame_altura = self.spritesheet.get_height()
        self.frame_atual = 0 
        self.contador = 0      
        self.image = self.spritesheet.subsurface(
        (0, 0, self.frame_largura, self.frame_altura)
        )
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_original = self.image

    def update(self):
        self.contador += 1
        if self.contador >= 12: 
            self.contador = 0
            self.frame_atual = (self.frame_atual + 1) % 3
            frame = self.spritesheet.subsurface(
                (self.frame_atual * self.frame_largura, 0, self.frame_largura, self.frame_altura)
            )
            self.image_original = pygame.transform.scale(frame, (self.width, self.height))

            if self.speed < 0:
                self.image = pygame.transform.flip(self.image_original, True, False)
            else:
                self.image = self.image_original
        self.x += self.speed
        if self.x > 800 - self.width:
            self.speed = -1.4
            self.image = pygame.transform.flip(self.image_original, True, False)
        if self.x < 0:
            self.speed = 1.4
            self.image = self.image_original

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        

