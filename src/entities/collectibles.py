import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def aplicar_efeito(self, player):
        ### Cada subclasse define o que acontece quando é coletado.
        ### Por padrão não faz nada — é tipo um 'contrato' que as filhas cumprem
        raise NotImplementedError("Subclasses devem implementar aplicar_efeito")

    def update(self, player):
        if self.collected:
            return
        if self.rect.colliderect(player.rect):
            self.collected = True
            self.aplicar_efeito(player)
            self.kill()  # remove o sprite de todos os grupos (some da tela)

class Carne(Collectible):
    def __init__(self, x, y, image, groups):
        super().__init__(x, y, image, groups)

    def aplicar_efeito(self, player):
        player.ganhar_vida()


class Carvao(Collectible):
    def __init__(self, x, y, image, groups):
        super().__init__(x, y, image, groups)

    def aplicar_efeito(self, player):
        player.coletar_carvao()


class Cerveja(Collectible):
    def __init__(self, x, y, image, groups, duracao_ms=5000, multiplicador=1.5):
        super().__init__(x, y, image, groups)
        self.duracao_ms = duracao_ms
        self.multiplicador = multiplicador

    def aplicar_efeito(self, player):
        player.aplicar_boost_velocidade(self.multiplicador, self.duracao_ms)