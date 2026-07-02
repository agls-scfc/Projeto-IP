import pygame
import design_mapa as mapa
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.collectibles import Carne, Carvao, Cerveja


# ------------------------- CONSTANTES DO JOGO -------------------------------

TILE        = mapa.TILE
SCREEN_W    = mapa.SCREEN_W
SCREEN_H    = mapa.SCREEN_H
FPS         = mapa.FPS

LINHA_CHAO  = 14                                  # a partir desta linha, pra baixo, e chao
MAP_LARGURA = mapa.MAP_COLS * TILE                # largura total do nivel em pixels

CARVOES_PARA_VENCER = 3                           # precisa de 3 carvoes pra vencer
# ATENCAO: o mapa hoje tem so 3 carvoes. Ate o time adicionar mais 2, o jogo
# nao e "vencivel". Pra testar a vitoria antes disso, baixe este numero.

INIMIGO_TAMANHO = 52                              # tamanho dos inimigos em pixels
MORTE_QUEDA_Y   = 480                             # se o Mario passar disso, caiu no buraco

INICIO_X = 2 * TILE                               # posicao inicial do Mario (coluna 2)
INICIO_Y = LINHA_CHAO * TILE - 60

BANDEIRA_LINHA, BANDEIRA_COL = mapa.BANDEIRA
BANDEIRA_X = BANDEIRA_COL * TILE

# cores dos coletaveis, uma por tipo
COR_CARNE  = (200,  40,  40)
COR_CARVAO = ( 60,  60,  60)
COR_BREJA  = (230, 180,  40)

# de que cor no mapa vem cada tipo, e qual classe usar pra cada um
TIPO_POR_COR = {"vermelha": "carne", "amarela": "carvao", "azul": "breja"}
CLASSE_POR_TIPO = {"carne": Carne, "carvao": Carvao, "breja": Cerveja}
COR_POR_TIPO = {"carne": COR_CARNE, "carvao": COR_CARVAO, "breja": COR_BREJA}


# ------------------- CONSTRUCAO DO MUNDO (a partir do mapa) ------------------

def col_eh_buraco(col):
    """Diz se uma coluna faz parte de algum buraco (onde o chao some)."""
    for c_inicio, c_fim in mapa.BURACOS:
        if c_inicio <= col <= c_fim:
            return True
    return False


def construir_solidos():
    """Cria a lista de retangulos solidos (chao, plataformas e escada)."""
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


def criar_imagem_coletavel(cor):
    """Cria uma imagenzinha (bolinha colorida) para um coletavel."""
    tam = 22
    img = pygame.Surface((tam, tam), pygame.SRCALPHA)
    pygame.draw.circle(img, cor, (tam // 2, tam // 2), tam // 2 - 1)
    pygame.draw.circle(img, (0, 0, 0), (tam // 2, tam // 2), tam // 2 - 1, 2)
    return img


def construir_coletaveis():
    """Le o mapa e cria os coletaveis usando as classes Carne, Carvao e Cerveja.
    Todos entram num grupo de sprites, que cuida de guardar e remover cada um."""
    grupo = pygame.sprite.Group()
    imagens = {tipo: criar_imagem_coletavel(cor) for tipo, cor in COR_POR_TIPO.items()}
    for linha, col, cor in mapa.COLETAVEIS:
        tipo = TIPO_POR_COR.get(cor, "carvao")
        x = col * TILE + 6
        y = linha * TILE + 6
        Classe = CLASSE_POR_TIPO[tipo]
        Classe(x, y, imagens[tipo], grupo)        # cria e ja adiciona no grupo
    return grupo


def construir_inimigos():
    """Le o mapa e cria os inimigos, cada um patrulhando um trecho perto de onde nasce."""
    lista = []
    for linha, col in mapa.INIMIGOS:
        x = col * TILE
        y = (linha + 1) * TILE - INIMIGO_TAMANHO
        alcance = 2 * TILE
        lista.append(Enemy(x, y, x - alcance, x + alcance, INIMIGO_TAMANHO))
    return lista


def criar_player():
    """Cria o Mario ja em pe no chao."""
    p = Player(INICIO_X, INICIO_Y)
    p.y = LINHA_CHAO * TILE - p.height
    return p


def novo_jogo():
    """Cria um estado de jogo do zero (usado no inicio e ao reiniciar)."""
    return {
        "player": criar_player(),
        "solidos": construir_solidos(),
        "coletaveis": construir_coletaveis(),     # grupo de sprites
        "inimigos": construir_inimigos(),          # lista de Enemy
        "cam_x": 0,
    }


# ------------------------------- LOGICA -------------------------------------

def resolver_colisao_vertical(player, solidos):
    """Impede o Mario de atravessar o chao e as plataformas."""
    player.no_chao = False
    caixa = pygame.Rect(int(player.x), int(player.y), player.width, player.height)
    for s in solidos:
        if caixa.colliderect(s):
            if player.velocidade_y > 0:            # caindo -> pousa em cima
                player.y = s.top - player.height
                player.velocidade_y = 0
                player.no_chao = True
            elif player.velocidade_y < 0:          # subindo -> bate a cabeca
                player.y = s.bottom
                player.velocidade_y = 0
            caixa = pygame.Rect(int(player.x), int(player.y), player.width, player.height)


def atualizar_playing(jogo):
    """Roda um quadro da logica. Devolve 'JOGANDO', 'VITORIA' ou 'GAMEOVER'."""
    player = jogo["player"]

    # 1) o Mario se move e cai
    player.update()

    # 2) colisao com o chao e as plataformas
    resolver_colisao_vertical(player, jogo["solidos"])

    # nao deixa sair do mapa pelos lados
    if player.x < 0:
        player.x = 0
    if player.x > MAP_LARGURA - player.width:
        player.x = MAP_LARGURA - player.width

    # deixa a caixa de colisao na posicao final antes de checar coletaveis e inimigos
    player.rect.topleft = (int(player.x), int(player.y))

    # 3) caiu num buraco? perde vida e volta ao inicio
    if player.y > MORTE_QUEDA_Y:
        player.vida -= 1
        player.voltar_para(INICIO_X, LINHA_CHAO * TILE - player.height)
        player.rect.topleft = (int(player.x), int(player.y))
        if player.vida <= 0:
            return "GAMEOVER"

    # 4) coletaveis: as proprias classes checam a colisao e aplicam o efeito
    jogo["coletaveis"].update(player)

    # 5) inimigos: pular em cima derrota; encostar de lado machuca
    for e in jogo["inimigos"]:
        if not e.vivo:
            continue
        e.update()
        if player.rect.colliderect(e.rect):
            caiu_em_cima = (player.velocidade_y > 0 and
                            player.rect.bottom <= e.rect.top + e.height // 2)
            if caiu_em_cima:
                e.vivo = False
                player.velocidade_y = -9           # quica pra cima
            else:
                player.levar_dano()
                if player.vida <= 0:
                    return "GAMEOVER"

    # 6) venceu? chegou na bandeira com os carvoes necessarios
    if player.x >= BANDEIRA_X and player.carvao >= CARVOES_PARA_VENCER:
        return "VITORIA"

    # 7) camera: acompanha o Mario, sem passar das bordas do mapa
    cam = player.x + player.width / 2 - SCREEN_W / 2
    jogo["cam_x"] = max(0, min(cam, MAP_LARGURA - SCREEN_W))
    return "JOGANDO"


# ------------------------------- DESENHO ------------------------------------

def desenhar_nuvem(tela, cx, cy):
    branco = (255, 255, 255)
    pygame.draw.circle(tela, branco, (cx, cy), 18)
    pygame.draw.circle(tela, branco, (cx + 20, cy + 4), 14)
    pygame.draw.circle(tela, branco, (cx - 20, cy + 4), 14)
    pygame.draw.rect(tela, branco, (cx - 20, cy, 40, 12))


def desenhar_fundo(tela, cam_x):
    """Fundo tematico do Brasil: predios verde-amarelos, nuvens e bandeirinhas."""
    base_y = LINHA_CHAO * TILE
    desloc = int(cam_x * 0.5)
    largura_p = 96
    cores = [(96, 130, 96), (196, 176, 86), (110, 140, 110), (206, 190, 96)]
    for i in range(-1, SCREEN_W // largura_p + 2):
        x = i * largura_p - (desloc % largura_p)
        idx = (i + desloc // largura_p) % len(cores)
        altura_p = 100 + idx * 16
        pygame.draw.rect(tela, cores[idx], (x, base_y - altura_p, largura_p - 10, altura_p))
        for jy in range(base_y - altura_p + 14, base_y - 14, 26):
            for jx in range(x + 12, x + largura_p - 20, 24):
                pygame.draw.rect(tela, (245, 240, 170), (jx, jy, 8, 12))
    desloc_n = int(cam_x * 0.25)
    for i in range(-1, SCREEN_W // 300 + 2):
        cx = i * 300 - (desloc_n % 300) + 100
        desenhar_nuvem(tela, cx, 80)
        desenhar_nuvem(tela, cx + 150, 150)
    largura_b = 28
    for i in range(SCREEN_W // largura_b + 1):
        x = i * largura_b
        cor = (0, 150, 60) if i % 2 == 0 else (255, 210, 0)
        pygame.draw.polygon(tela, cor, [(x, 0), (x + largura_b, 0), (x + largura_b // 2, 20)])


def desenhar_mundo(tela, cam_x):
    col_ini = max(0, int(cam_x // TILE) - 1)
    col_fim = min(mapa.MAP_COLS, int((cam_x + SCREEN_W) // TILE) + 2)
    for col in range(col_ini, col_fim):
        if not col_eh_buraco(col):
            for linha in range(LINHA_CHAO, mapa.MAP_ROWS):
                cor = mapa.COR_CHAO_TOP if linha == LINHA_CHAO else mapa.COR_CHAO
                pygame.draw.rect(tela, cor, (col * TILE - cam_x, linha * TILE, TILE, TILE))
    for linha, c_inicio, c_fim in mapa.PLATAFORMAS:
        for col in range(c_inicio, c_fim + 1):
            x = col * TILE - cam_x
            if -TILE <= x <= SCREEN_W:
                pygame.draw.rect(tela, mapa.COR_PLAT, (x, linha * TILE, TILE, TILE))
                pygame.draw.rect(tela, mapa.COR_PLAT_TOP, (x, linha * TILE, TILE, 6))
    for col, altura in mapa.ESCADA:
        for i in range(altura):
            linha = 13 - i
            x = col * TILE - cam_x
            if -TILE <= x <= SCREEN_W:
                pygame.draw.rect(tela, mapa.COR_CHAO, (x, linha * TILE, TILE, TILE))
                pygame.draw.rect(tela, mapa.COR_CHAO_TOP, (x, linha * TILE, TILE, 6))


def desenhar_bandeira(tela, cam_x):
    x = BANDEIRA_X - cam_x
    if -TILE <= x <= SCREEN_W:
        topo = (BANDEIRA_LINHA - 4) * TILE
        base = LINHA_CHAO * TILE
        pygame.draw.rect(tela, (230, 230, 230), (x, topo, 4, base - topo))
        pygame.draw.polygon(tela, (0, 160, 0),
                            [(x + 4, topo), (x + 4 + 26, topo + 10), (x + 4, topo + 20)])


def desenhar_coletaveis(tela, cam_x, grupo):
    """Desenha os coletaveis que ainda estao no grupo (os pegos ja sairam)."""
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
    """Painel com vidas e a contagem de cada coletavel."""
    linhas = [
        "Vidas: {}".format(player.vida),
        "Carne: {}".format(player.carne),
        "Carvao: {}/{}".format(player.carvao, CARVOES_PARA_VENCER),
        "Breja: {}".format(player.cerveja),
    ]
    y = 8
    for texto in linhas:
        tela.blit(fonte.render(texto, True, (0, 0, 0)), (10, y))
        y += 24
    if player.boost_ativo():
        tela.blit(fonte.render("BOOST!", True, (200, 120, 0)), (10, y))


def desenhar_jogo(tela, fonte, jogo):
    cam_x = jogo["cam_x"]
    player = jogo["player"]
    tela.fill(mapa.COR_CEU)
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
    tela = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Super Mario Carne")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 28)
    fonte_grande = pygame.font.SysFont(None, 64)

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