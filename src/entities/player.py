import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 45
        self.height = 45
        self.speed = 2
        self.velocidade_y = 0
        self.no_chao = True

        # sprites
        self.sheet_walk = pygame.image.load("src/images/playerwalksprites.png").convert_alpha()
        self.sheet_jump = pygame.image.load("src/images/playerjumpsprites.png").convert_alpha()

        # dimensões dos frames
        self.frame_largura_walk = self.sheet_walk.get_width() // 3
        self.frame_largura_jump = self.sheet_jump.get_width() // 3
        self.frame_altura = self.sheet_walk.get_height()

        # controle de animação
        self.frame_atual = 0
        self.contador = 0
        self.virado = False

        # imagem inicial
        self.image_original = self._get_frame(self.sheet_walk, 0, self.frame_largura_walk)
        self.image = self.image_original

    def _get_frame(self, sheet, frame, largura):
        frame_surf = sheet.subsurface((frame * largura, 0, largura, self.frame_altura))
        return pygame.transform.scale(frame_surf, (self.width, self.height))

    def update(self):
        teclas = pygame.key.get_pressed()
        movendo = False

        if teclas[pygame.K_LEFT]:
            self.x -= self.speed
            self.virado = True
            movendo = True
        if teclas[pygame.K_RIGHT]:
            self.x += self.speed
            self.virado = False
            movendo = True
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = -10
            self.no_chao = False

        if not self.no_chao:
            sheet = self.sheet_jump
            largura = self.frame_largura_jump
        else:
            sheet = self.sheet_walk
            largura = self.frame_largura_walk

        if movendo or not self.no_chao:
            self.contador += 1
            limite = 50 if not self.no_chao else 12
            if self.contador >= limite:
                self.contador = 0
                self.frame_atual = (self.frame_atual + 1) % 3

        self.image_original = self._get_frame(sheet, self.frame_atual, largura)

        if self.virado:
            self.image = pygame.transform.flip(self.image_original, True, False)
        else:
            self.image = self.image_original

        # gravidade
        self.velocidade_y += 0.5
        self.y += self.velocidade_y

        if self.y >= 500:
            self.y = 500
            self.velocidade_y = 0
            self.no_chao = True
            

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))