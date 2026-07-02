import pygame


class Player:
    VIDA_MAX = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60          # tamanho do Mario
        self.height = 60

        # movimento e fisica
        self.speed_base = 4      # velocidade normal de andar
        self.speed = self.speed_base
        self.velocidade_y = 0
        self.no_chao = True

        # estado do jogo (mexido pelos coletaveis e pelos inimigos)
        self.vida = self.VIDA_MAX
        self.carne = 0           # quantas carnes pegou
        self.carvao = 0          # quantos carvoes pegou
        self.cerveja = 0         # quantas cervejas pegou
        self.invuln_timer = 0    # quadros de invencibilidade apos tomar dano

        # boost de velocidade (dado pela cerveja)
        self.boost_mult = 1.0
        self.boost_ate = 0       # instante (em ms) em que o boost acaba

        # caixa de colisao, acompanha a posicao do Mario
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # sprites e animacao
        self.sheet_walk = pygame.image.load("src/images/playerwalksprites.png").convert_alpha()
        self.sheet_jump = pygame.image.load("src/images/playerjumpsprites.png").convert_alpha()
        self.frame_largura_walk = self.sheet_walk.get_width() // 3
        self.frame_largura_jump = self.sheet_jump.get_width() // 3
        self.frame_altura = self.sheet_walk.get_height()
        self.frame_atual = 0
        self.contador = 0
        self.virado = False
        self.image_original = self._get_frame(self.sheet_walk, 0, self.frame_largura_walk)
        self.image = self.image_original

    # ---------------- metodos chamados pelos COLETAVEIS ----------------
    def ganhar_vida(self):
        """Chamado pela Carne: conta a carne e recupera 1 vida (ate o maximo)."""
        self.carne += 1
        self.vida = min(self.vida + 1, self.VIDA_MAX)

    def coletar_carvao(self):
        """Chamado pelo Carvao: conta o carvao (objetivo do nivel)."""
        self.carvao += 1

    def aplicar_boost_velocidade(self, multiplicador, duracao_ms):
        """Chamado pela Cerveja: conta a cerveja e liga o boost por um tempo."""
        self.cerveja += 1
        self.boost_mult = multiplicador
        self.boost_ate = pygame.time.get_ticks() + duracao_ms

    def boost_ativo(self):
        """Diz se o boost de velocidade ainda esta valendo."""
        return pygame.time.get_ticks() < self.boost_ate

    # ---------------- metodos chamados pela MAIN ----------------
    def levar_dano(self):
        """Tira 1 vida (se nao estiver invencivel) e liga a invencibilidade."""
        if self.invuln_timer == 0:
            self.vida -= 1
            self.invuln_timer = 60          # cerca de 1 segundo protegido

    def voltar_para(self, x, y):
        """Reposiciona o Mario (usado ao cair no buraco)."""
        self.x = x
        self.y = y
        self.velocidade_y = 0

    # ---------------- animacao interna ----------------
    def _get_frame(self, sheet, frame, largura):
        frame_surf = sheet.subsurface((frame * largura, 0, largura, self.frame_altura))
        return pygame.transform.scale(frame_surf, (self.width, self.height))

    def update(self):
        # velocidade atual (com boost, se estiver ativo)
        self.speed = self.speed_base * self.boost_mult if self.boost_ativo() else self.speed_base

        # a invencibilidade vai passando
        if self.invuln_timer > 0:
            self.invuln_timer -= 1

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
            self.velocidade_y = -13          # forca do pulo
            self.no_chao = False

        # escolhe a folha de sprites (andando ou pulando) e anima
        if not self.no_chao:
            sheet, largura = self.sheet_jump, self.frame_largura_jump
        else:
            sheet, largura = self.sheet_walk, self.frame_largura_walk
        if movendo or not self.no_chao:
            self.contador += 1
            limite = 50 if not self.no_chao else 12
            if self.contador >= limite:
                self.contador = 0
                self.frame_atual = (self.frame_atual + 1) % 3
        self.image_original = self._get_frame(sheet, self.frame_atual, largura)
        self.image = pygame.transform.flip(self.image_original, True, False) if self.virado else self.image_original

        # gravidade
        self.velocidade_y += 0.5
        self.y += self.velocidade_y

        # mantem a caixa de colisao junto do Mario
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))