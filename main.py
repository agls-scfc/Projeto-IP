import pygame
from src.script import design_mapa as mapa
from src.script.player import Player
from src.script.enemy import Enemy
from src.script.collectibles import Carne, Carvao, Cerveja


# ------------------------- CONSTANTES DO JOGO -------------------------------

TILE        = mapa.TILE
SCREEN_W    = mapa.SCREEN_W
SCREEN_H    = mapa.SCREEN_H
FPS         = mapa.FPS

LINHA_CHAO  = 14
MAP_LARGURA = mapa.MAP_COLS * TILE

CARVOES_PARA_VENCER = 6           # quantos carvoes precisa pra vencer
INIMIGO_TAMANHO = 60              # tamanho dos inimigos em pixels
TAM_COLETAVEL   = 50              # tamanho dos coletaveis na tela
MORTE_QUEDA_Y   = 480

INICIO_X = 2 * TILE
INICIO_Y = LINHA_CHAO * TILE - 60

BANDEIRA_LINHA, BANDEIRA_COL = mapa.BANDEIRA
BANDEIRA_X = BANDEIRA_COL * TILE

# qual classe usar para cada cor de coletavel do mapa
TIPO_POR_COR = {"vermelha": "carne", "amarela": "carvao", "azul": "breja"}
CLASSE_POR_TIPO = {"carne": Carne, "carvao": Carvao, "breja": Cerveja}


# ------------------------- IMAGENS (carregadas 1x) --------------------------

IMAGENS = {}

def carregar_imagens():
    """Carrega e ajusta todas as imagens do jogo uma unica vez."""
    def load(nome):
        return pygame.image.load("src/images/" + nome).convert_alpha()

    # coletaveis (versao colorida, para desenhar no mapa)
    IMAGENS["carne"]  = pygame.transform.smoothscale(load("coletavelbifecores.png"),    (TAM_COLETAVEL, TAM_COLETAVEL))
    IMAGENS["carvao"] = pygame.transform.smoothscale(load("coletavelcarvaocores.png"),  (TAM_COLETAVEL, TAM_COLETAVEL))
    IMAGENS["breja"]  = pygame.transform.smoothscale(load("coletavelcervejacores.png"), (TAM_COLETAVEL, TAM_COLETAVEL))

    # icones do HUD (carvao colorido = pego, carvao cinza = faltando)
    IMAGENS["hud_carvao"]       = pygame.transform.smoothscale(load("coletavelcarvaocores.png"),  (26, 26))
    IMAGENS["hud_carvao_cinza"] = pygame.transform.smoothscale(load("coletavelcarvaocinza.png"),  (26, 26))
    IMAGENS["hud_carne"]        = pygame.transform.smoothscale(load("coletavelbifecores.png"),    (26, 26))
    IMAGENS["hud_carne_cinza"]  = pygame.transform.smoothscale(load("coletavelbifecinza.png"),    (26, 26))
    IMAGENS["hud_breja"]        = pygame.transform.smoothscale(load("coletavelcervejacores.png"), (26, 26))
    IMAGENS["hud_breja_cinza"]  = pygame.transform.smoothscale(load("coletavelcervejacinza.png"), (26, 26))

    # cenario de fundo, esticado para cobrir o nivel inteiro
    IMAGENS["fundo"] = pygame.transform.smoothscale(load("planodefundo.png"), (MAP_LARGURA, SCREEN_H))


# ------------------- CONSTRUCAO DO MUNDO (a partir do mapa) ------------------

def col_eh_buraco(col):
    for c_inicio, c_fim in mapa.BURACOS:
        if c_inicio <= col <= c_fim:
            return True
    return False


def construir_solidos():
    solidos = []
    altura_chao = (mapa.MAP_ROWS - LINHA_CHAO) * TILE
    for col in range(mapa.MAP_COLS):
        if not col_eh_buraco(col):
            solidos.append(pygame.Rect(col * TILE, LINHA_CHAO * TILE, TILE, altura_chao))
    for linha, c_inicio, c_fim in mapa.PLATAFORMAS:
        largura = (c_fim - c_inicio + 1) * TILE
        solidos.append(pygame.Rect(c_inicio * TILE, linha * TILE, largura, TILE))
    for col, altura in mapa.ESCADA:
        topo = 14 - altura
        solidos.append(pygame.Rect(col * TILE, topo * TILE, TILE, altura * TILE))
    return solidos


def construir_coletaveis():
    """Le o mapa e cria os coletaveis (classes do time) com as imagens reais."""
    grupo = pygame.sprite.Group()
    for linha, col, cor in mapa.COLETAVEIS:
        tipo = TIPO_POR_COR.get(cor, "carvao")
        img = IMAGENS[tipo]
        x = col * TILE + (TILE - img.get_width()) // 2       # centraliza na casa
        y = linha * TILE + (TILE - img.get_height()) // 2
        CLASSE_POR_TIPO[tipo](x, y, img, grupo)
    return grupo


def construir_inimigos():
    lista = []
    for linha, col in mapa.INIMIGOS:
        x = col * TILE
        y = (linha + 1) * TILE - INIMIGO_TAMANHO
        alcance = 2 * TILE
        lista.append(Enemy(x, y, x - alcance, x + alcance, INIMIGO_TAMANHO))
    return lista


def criar_player():
    p = Player(INICIO_X, INICIO_Y)
    p.y = LINHA_CHAO * TILE - p.height
    return p


def novo_jogo():
    if not IMAGENS:
        carregar_imagens()
    return {
        "player": criar_player(),
        "solidos": construir_solidos(),
        "coletaveis": construir_coletaveis(),
        "inimigos": construir_inimigos(),
        "cam_x": 0,
    }


# ------------------------------- LOGICA -------------------------------------

def resolver_colisao_vertical(player, solidos):
    # resolve a sobreposicao vertical: pousar em cima ou bater a cabeca
    caixa = pygame.Rect(int(player.x), int(player.y), player.width, player.height)
    for s in solidos:
        if caixa.colliderect(s):
            if player.velocidade_y > 0:
                player.y = s.top - player.height
                player.velocidade_y = 0
            elif player.velocidade_y < 0:
                player.y = s.bottom
                player.velocidade_y = 0
            caixa = pygame.Rect(int(player.x), int(player.y), player.width, player.height)

    # Checa o chao com uma "sola" 3px abaixo dos pes, para um apoio ESTAVEL.
    # Sem isto o player oscilava entre no-ar/no-chao a cada quadro, e o sprite
    # piscava entre andar e pular (era isso que parecia tremor).
    sola = pygame.Rect(int(player.x) + 4, int(player.y) + player.height, player.width - 8, 3)
    apoio = None
    for s in solidos:
        if sola.colliderect(s):
            apoio = s
            break
    if apoio is not None:
        player.no_chao = True
        if player.velocidade_y >= 0:
            player.y = apoio.top - player.height   # cola no chao, elimina o tremor
            player.velocidade_y = 0
    else:
        player.no_chao = False


def atualizar_playing(jogo):
    player = jogo["player"]
    player.update()
    resolver_colisao_vertical(player, jogo["solidos"])

    if player.x < 0:
        player.x = 0
    if player.x > MAP_LARGURA - player.width:
        player.x = MAP_LARGURA - player.width
    player.rect.topleft = (int(player.x), int(player.y))

    if player.y > MORTE_QUEDA_Y:
        player.vida -= 1
        player.voltar_para(INICIO_X, LINHA_CHAO * TILE - player.height)
        player.rect.topleft = (int(player.x), int(player.y))
        if player.vida <= 0:
            return "GAMEOVER"

    jogo["coletaveis"].update(player)

    for e in jogo["inimigos"]:
        if not e.vivo:
            continue
        e.update()
        if player.rect.colliderect(e.rect):
            caiu_em_cima = (player.velocidade_y > 0 and
                            player.rect.bottom <= e.rect.top + e.height // 2)
            if caiu_em_cima:
                e.vivo = False
                player.velocidade_y = -9
            else:
                player.levar_dano()
                if player.vida <= 0:
                    return "GAMEOVER"

    if player.x >= BANDEIRA_X and player.carvao >= CARVOES_PARA_VENCER:
        return "VITORIA"

    cam = player.x + player.width / 2 - SCREEN_W / 2
    jogo["cam_x"] = max(0, min(cam, MAP_LARGURA - SCREEN_W))
    return "JOGANDO"


# ------------------------------- DESENHO ------------------------------------

def desenhar_fundo(tela, cam_x):
    """Desenha o pedaco visivel do cenario (planodefundo.png)."""
    tela.blit(IMAGENS["fundo"], (0, 0), area=(int(cam_x), 0, SCREEN_W, SCREEN_H))


def desenhar_mundo(tela, cam_x):
    """Desenha o chao e os buracos por cima do cenario, e as plataformas."""
    col_ini = max(0, int(cam_x // TILE) - 1)
    col_fim = min(mapa.MAP_COLS, int((cam_x + SCREEN_W) // TILE) + 2)
    for col in range(col_ini, col_fim):
        x = col * TILE - cam_x
        if col_eh_buraco(col):
            # buraco: pinta de ceu para virar um vao de verdade
            pygame.draw.rect(tela, mapa.COR_CEU, (x, LINHA_CHAO * TILE, TILE, SCREEN_H - LINHA_CHAO * TILE))
        else:
            for linha in range(LINHA_CHAO, mapa.MAP_ROWS):
                cor = mapa.COR_CHAO_TOP if linha == LINHA_CHAO else mapa.COR_CHAO
                pygame.draw.rect(tela, cor, (x, linha * TILE, TILE, TILE))

    for linha, c_inicio, c_fim in mapa.PLATAFORMAS:
        for col in range(c_inicio, c_fim + 1):
            x = col * TILE - cam_x
            if -TILE <= x <= SCREEN_W:
                pygame.draw.rect(tela, mapa.COR_PLAT, (x, linha * TILE, TILE, TILE))
                pygame.draw.rect(tela, mapa.COR_PLAT_TOP, (x, linha * TILE, TILE, 6))


def desenhar_bandeira(tela, cam_x):
    x = BANDEIRA_X - cam_x
    if -TILE <= x <= SCREEN_W:
        topo = (BANDEIRA_LINHA - 4) * TILE
        base = LINHA_CHAO * TILE
        pygame.draw.rect(tela, (230, 230, 230), (x, topo, 4, base - topo))
        pygame.draw.polygon(tela, (0, 160, 0),
                            [(x + 4, topo), (x + 4 + 26, topo + 10), (x + 4, topo + 20)])


def desenhar_coletaveis(tela, cam_x, grupo):
    for c in grupo:
        x = c.rect.x - cam_x
        if -TILE <= x <= SCREEN_W:
            tela.blit(c.image, (x, c.rect.y))


def desenhar_inimigos(tela, cam_x, inimigos):
    for e in inimigos:
        if not e.vivo:
            continue
        x = e.x - cam_x
        if -TILE <= x <= SCREEN_W:
            tela.blit(e.image, (x, e.y))


def desenhar_hud(tela, fonte, player):
    """HUD em icones, sem painel de fundo.
    Carne = vida do player (colorida = tem, cinza = perdeu).
    Carvao = progresso rumo a vitoria.
    Breja = 1 icone: colorida quando o boost esta ativo, cinza quando nao."""
    preto = (0, 0, 0)

    # CARNE = vida (3 no total)
    tela.blit(fonte.render("Carne:", True, preto), (10, 10))
    x = 92
    for i in range(3):
        icone = IMAGENS["hud_carne"] if i < player.vida else IMAGENS["hud_carne_cinza"]
        tela.blit(icone, (x, 8))
        x += 30

    # CARVAO = progresso (nao mexemos, continua igual)
    tela.blit(fonte.render("Carvao:", True, preto), (10, 42))
    x = 92
    for i in range(CARVOES_PARA_VENCER):
        icone = IMAGENS["hud_carvao"] if i < player.carvao else IMAGENS["hud_carvao_cinza"]
        tela.blit(icone, (x, 40))
        x += 30

    # BREJA = 1 icone: colorida com boost ativo, cinza sem boost
    tela.blit(fonte.render("Breja:", True, preto), (10, 74))
    icone = IMAGENS["hud_breja"] if player.boost_ativo() else IMAGENS["hud_breja_cinza"]
    tela.blit(icone, (92, 72))


def desenhar_jogo(tela, fonte, jogo):
    cam_x = jogo["cam_x"]
    player = jogo["player"]
    desenhar_fundo(tela, cam_x)
    desenhar_mundo(tela, cam_x)
    desenhar_bandeira(tela, cam_x)
    desenhar_coletaveis(tela, cam_x, jogo["coletaveis"])
    desenhar_inimigos(tela, cam_x, jogo["inimigos"])
    piscando = player.invuln_timer > 0 and (player.invuln_timer // 5) % 2 == 0
    if not piscando:
        tela.blit(player.image, (player.x - cam_x, player.y))
    desenhar_hud(tela, fonte, player)


def desenhar_texto_centro(tela, fonte, texto, cor, y):
    img = fonte.render(texto, True, cor)
    tela.blit(img, (SCREEN_W // 2 - img.get_width() // 2, y))


def desenhar_menu(tela, fonte_grande, fonte):
    if IMAGENS:
        desenhar_fundo(tela, 0)
    else:
        tela.fill(mapa.COR_CEU)
    desenhar_texto_centro(tela, fonte_grande, "Super Mario Carne", (0, 0, 0), 200)
    desenhar_texto_centro(tela, fonte, "Aperte ENTER para comecar", (0, 0, 0), 300)
    desenhar_texto_centro(tela, fonte, "Setas para andar, ESPACO para pular", (0, 0, 0), 340)


def desenhar_overlay(tela, fonte_grande, fonte, titulo, cor, subtitulo):
    veu = pygame.Surface((SCREEN_W, SCREEN_H))
    veu.set_alpha(150)
    veu.fill((0, 0, 0))
    tela.blit(veu, (0, 0))
    desenhar_texto_centro(tela, fonte_grande, titulo, cor, 220)
    desenhar_texto_centro(tela, fonte, subtitulo, (255, 255, 255), 300)


# ------------------------------- LACO PRINCIPAL -----------------------------

def main():
    pygame.init()
    pygame.mixer.init()                    # liga o sistema de audio
    tela = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Super Mario Carne")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 28)
    fonte_grande = pygame.font.SysFont(None, 64)

    carregar_imagens()

    # trilha sonora em loop infinito
    pygame.mixer.music.load("src/musica/trilhasonora.mp3")
    pygame.mixer.music.set_volume(0.5)     # volume de 0.0 a 1.0
    pygame.mixer.music.play(-1)            # -1 = repete pra sempre
    estado = "MENU"
    jogo = novo_jogo()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                if estado in ("MENU", "VITORIA", "GAMEOVER"):
                    jogo = novo_jogo()
                    estado = "JOGANDO"

        if estado == "JOGANDO":
            estado = atualizar_playing(jogo)

        if estado == "MENU":
            desenhar_menu(tela, fonte_grande, fonte)
        else:
            desenhar_jogo(tela, fonte, jogo)
            if estado == "VITORIA":
                desenhar_overlay(tela, fonte_grande, fonte, "Voce venceu!", (80, 255, 80),
                                 "Aperte ENTER para jogar de novo")
            elif estado == "GAMEOVER":
                desenhar_overlay(tela, fonte_grande, fonte, "Game Over", (255, 80, 80),
                                 "Aperte ENTER para tentar de novo")

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()