import pygame


class Enemy:
    def __init__(self, x, y, min_x, max_x, tamanho=52):
        self.x = x
        self.y = y
        self.width = tamanho
        self.height = tamanho
        self.min_x = min_x        # limite esquerdo da patrulha
        self.max_x = max_x        # limite direito da patrulha
        self.speed = 1.4
        self.dir = 1              # 1 = indo pra direita, -1 = pra esquerda
        self.vivo = True

        # caixa de colisao
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)

        # sprites e animacao
        self.spritesheet = pygame.image.load("src/images/inimigosprites.png").convert_alpha()
        self.frame_largura = self.spritesheet.get_width() // 3
        self.frame_altura = self.spritesheet.get_height()
        self.frame_atual = 0
        self.contador = 0
        self.image = self._get_frame(0)

    def _get_frame(self, i):
        f = self.spritesheet.subsurface((i * self.frame_largura, 0, self.frame_largura, self.frame_altura))
        return pygame.transform.scale(f, (self.width, self.height))

    def update(self):
        # animacao
        self.contador += 1
        if self.contador >= 12:
            self.contador = 0
            self.frame_atual = (self.frame_atual + 1) % 3
        base = self._get_frame(self.frame_atual)
        self.image = base if self.dir > 0 else pygame.transform.flip(base, True, False)

        # patrulha entre os limites (nao depende mais da largura da tela)
        self.x += self.speed * self.dir
        if self.x < self.min_x or self.x > self.max_x:
            self.dir *= -1

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))