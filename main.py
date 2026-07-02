# ============================================================================
#  SUPER MARIO CARNE  -  arquivo principal (main) do jogo
# ============================================================================
#  Este arquivo e o "maestro" do jogo. Ele nao desenha o Mario nem move o
#  inimigo sozinho: ele cria os objetos, roda o laco principal (o game loop)
#  e coordena tudo (mundo, camera, colisoes, coletaveis, inimigos, vidas e
#  as telas de menu, vitoria e game over).
#
#  ---------------------------------------------------------------------------
#  O QUE ESTE ARQUIVO ESPERA DOS ARQUIVOS DA EQUIPE (o "contrato"):
#
#  - src/entities/player.py -> classe Player(x, y) com:
#       .update()  : le o teclado, aplica a gravidade e atualiza x, y
#       .image     : a imagem (sprite) atual do Mario
#       .x, .y, .width, .height, .speed, .velocidade_y, .no_chao
#    Obs: esta main funciona mesmo que o Player ainda tenha o "chao fixo"
#    em y = 500, porque ela mesma decide onde o Mario pousa. Mas o ideal e
#    o colega remover esse trecho (o chao de verdade vem do mapa).
#
#  Os inimigos e os coletaveis, por enquanto, sao controlados aqui dentro
#  da main (a partir do mapa), porque as classes deles ainda nao guardam o
#  tipo (carne/carvao/breja) nem tem patrulha. Quando essas classes ficarem
#  prontas, da pra trocar por elas nos pontos comentados abaixo.
# ============================================================================

import pygame
import design_mapa as mapa                      # dados e constantes do mapa (equipe)
from src.entities.player import Player          # classe do Mario (equipe)


# ------------------------- CONSTANTES DO JOGO -------------------------------

TILE       = mapa.TILE                          # tamanho de cada casa do mapa (32 px)
SCREEN_W   = mapa.SCREEN_W                       # largura da janela (800)
SCREEN_H   = mapa.SCREEN_H                       # altura da janela (576)
FPS        = mapa.FPS                            # quadros por segundo (60)

LINHA_CHAO = 14                                  # a partir desta linha, pra baixo, e chao
MAP_LARGURA = mapa.MAP_COLS * TILE               # largura total do nivel em pixels

VIDA_MAXIMA        = 3                            # teto de vidas (regra do grupo)
VIDAS_INICIAIS     = 3                            # comeca com 3 vidas
CARVOES_PARA_VENCER = 5                           # precisa de 5 carvoes pra vencer
# ATENCAO: o mapa hoje tem so 3 carvoes. Enquanto o time nao adicionar mais 2,
# o jogo nao e "vencivel". Pra testar a vitoria antes disso, baixe este numero.

DURACAO_BOOST = 5 * FPS                           # boost da breja dura 5 segundos
VELOCIDADE_NORMAL = 5                             # velocidade normal do Mario
VELOCIDADE_BOOST  = 9                             # velocidade durante o boost

MORTE_QUEDA_Y = 480
INIMIGO_TAMANHO = 52                              # tamanho dos inimigos em pixels                               # se o Mario passar disso, caiu no buraco

# posicao inicial do Mario (coluna 2, em cima do chao)
INICIO_X = 2 * TILE
INICIO_Y = LINHA_CHAO * TILE - 45                 # 45 = altura do Mario

# coluna da bandeira de chegada (fim do nivel)
BANDEIRA_LINHA, BANDEIRA_COL = mapa.BANDEIRA
BANDEIRA_X = BANDEIRA_COL * TILE

# cores dos coletaveis, uma por tipo (pra ficarem visualmente diferentes)
COR_CARNE  = (200,  40,  40)                       # vermelho
COR_CARVAO = ( 60,  60,  60)                       # cinza escuro
COR_BREJA  = (230, 180,  40)                       # ambar

# de que cor no mapa vem cada tipo de coletavel
TIPO_POR_COR = {"vermelha": "carne", "amarela": "carvao", "azul": "breja"}
COR_DO_TIPO  = {"carne": COR_CARNE, "carvao": COR_CARVAO, "breja": COR_BREJA}


# ------------------- CONSTRUCAO DO MUNDO (a partir do mapa) ------------------

def col_eh_buraco(col):
    """Diz se uma coluna faz parte de algum buraco (onde o chao some)."""
    for c_inicio, c_fim in mapa.BURACOS:
        if c_inicio <= col <= c_fim:
            return True
    return False


def construir_solidos():
    """Cria a lista de retangulos solidos (chao, plataformas e escada).
    Sao contra o que o Mario colide pra nao atravessar o chao."""
    solidos = []

    # chao: uma caixa por coluna, pulando os buracos
    altura_chao = (mapa.MAP_ROWS - LINHA_CHAO) * TILE
    for col in range(mapa.MAP_COLS):
        if not col_eh_buraco(col):
            solidos.append(pygame.Rect(col * TILE, LINHA_CHAO * TILE, TILE, altura_chao))

    # plataformas: uma caixa por plataforma
    for linha, c_inicio, c_fim in mapa.PLATAFORMAS:
        largura = (c_fim - c_inicio + 1) * TILE
        solidos.append(pygame.Rect(c_inicio * TILE, linha * TILE, largura, TILE))

    # escada: blocos empilhados sobre o chao, perto da bandeira
    for col, altura in mapa.ESCADA:
        topo = 14 - altura
        solidos.append(pygame.Rect(col * TILE, topo * TILE, TILE, altura * TILE))

    return solidos


def construir_coletaveis():
    """Le a lista de coletaveis do mapa e transforma em objetos com posicao e tipo."""
    lista = []
    for linha, col, cor in mapa.COLETAVEIS:
        tipo = TIPO_POR_COR.get(cor, "carvao")
        rect = pygame.Rect(col * TILE + 6, linha * TILE + 6, 20, 20)
        lista.append({"rect": rect, "tipo": tipo, "coletado": False})
    return lista


def construir_inimigos():
    """Le a lista de inimigos do mapa. Cada um patrulha um trecho perto de onde nasce."""
    lista = []
    for linha, col in mapa.INIMIGOS:
        largura, altura = INIMIGO_TAMANHO, INIMIGO_TAMANHO
        x = col * TILE
        y = (linha + 1) * TILE - altura                 # deixa os pes na superficie de baixo
        alcance = 2 * TILE                              # patrulha 2 casas pra cada lado
        lista.append({
            "x": float(x), "y": float(y), "w": largura, "h": altura,
            "dir": 1, "vel": 1.4, "vivo": True,
            "min_x": x - alcance, "max_x": x + alcance,
        })
    return lista


def carregar_sprite_inimigo():
    """Pega o primeiro quadro da spritesheet do inimigo, so pra desenhar."""
    sheet = pygame.image.load("src/images/inimigosprites.png").convert_alpha()
    largura = sheet.get_width() // 3
    altura = sheet.get_height()
    frame = sheet.subsurface((0, 0, largura, altura))
    return pygame.transform.scale(frame, (INIMIGO_TAMANHO, INIMIGO_TAMANHO))


def criar_player():
    """Cria o Mario ja em pe no chao, seja qual for o tamanho dele."""
    p = Player(INICIO_X, INICIO_Y)
    p.y = LINHA_CHAO * TILE - p.height
    return p


def novo_jogo():
    """Cria um estado de jogo do zero (usado no inicio e ao reiniciar)."""
    return {
        "player": criar_player(),
        "solidos": construir_solidos(),
        "coletaveis": construir_coletaveis(),
        "inimigos": construir_inimigos(),
        "sprite_inimigo": carregar_sprite_inimigo(),
        "vidas": VIDAS_INICIAIS,
        "contagem": {"carne": 0, "carvao": 0, "breja": 0},
        "boost_timer": 0,          # quadros restantes de boost da breja
        "invuln_timer": 0,         # quadros de invencibilidade apos tomar dano
        "cam_x": 0,                # posicao da camera (o quanto o mapa "andou")
    }


# ------------------------------- LOGICA -------------------------------------

def rect_do_player(player):
    """Monta a caixa de colisao do Mario a partir da posicao atual dele."""
    return pygame.Rect(int(player.x), int(player.y), player.width, player.height)


def resolver_colisao_vertical(player, solidos):
    """Impede o Mario de atravessar o chao e as plataformas.
    Se ele estava caindo, pousa em cima. Se estava subindo, bate a cabeca."""
    player.no_chao = False
    caixa = rect_do_player(player)
    for s in solidos:
        if caixa.colliderect(s):
            if player.velocidade_y > 0:            # caindo -> pousa em cima do solido
                player.y = s.top - player.height
                player.velocidade_y = 0
                player.no_chao = True
            elif player.velocidade_y < 0:          # subindo -> bate a cabeca
                player.y = s.bottom
                player.velocidade_y = 0
            caixa = rect_do_player(player)


def voltar_ao_inicio(player):
    """Coloca o Mario de volta no comeco do nivel (usado ao cair no buraco)."""
    player.x = INICIO_X
    player.y = LINHA_CHAO * TILE - player.height
    player.velocidade_y = 0


def atualizar_playing(jogo):
    """Roda um quadro da logica do jogo. Devolve o proximo estado
    ('JOGANDO', 'VITORIA' ou 'GAMEOVER')."""
    player = jogo["player"]

    # 1) o Mario se move e cai (input + gravidade estao dentro do update dele)
    player.update()

    # 2) colisao com o chao e as plataformas
    resolver_colisao_vertical(player, jogo["solidos"])

    # nao deixa sair pela esquerda nem passar do fim do mapa
    if player.x < 0:
        player.x = 0
    if player.x > MAP_LARGURA - player.width:
        player.x = MAP_LARGURA - player.width

    # 3) caiu num buraco? perde vida e volta ao inicio
    if player.y > MORTE_QUEDA_Y:
        jogo["vidas"] -= 1
        voltar_ao_inicio(player)
        if jogo["vidas"] <= 0:
            return "GAMEOVER"

    caixa = rect_do_player(player)

    # 4) coletaveis: se encostou, conta e aplica o efeito
    for c in jogo["coletaveis"]:
        if not c["coletado"] and caixa.colliderect(c["rect"]):
            c["coletado"] = True
            tipo = c["tipo"]
            jogo["contagem"][tipo] += 1
            if tipo == "carne":
                jogo["vidas"] = min(jogo["vidas"] + 1, VIDA_MAXIMA)   # recupera vida ate 3
            elif tipo == "breja":
                jogo["boost_timer"] = DURACAO_BOOST                   # liga o boost por 5s

    # 5) boost da breja: enquanto durar, o Mario anda mais rapido
    if jogo["boost_timer"] > 0:
        jogo["boost_timer"] -= 1
        player.speed = VELOCIDADE_BOOST
    else:
        player.speed = VELOCIDADE_NORMAL

    # 6) invencibilidade temporaria (logo depois de tomar dano de um inimigo)
    if jogo["invuln_timer"] > 0:
        jogo["invuln_timer"] -= 1

    # 7) inimigos: patrulham; pular em cima derrota, encostar de lado machuca
    for e in jogo["inimigos"]:
        if not e["vivo"]:
            continue                                                 # inimigo ja derrotado
        e["x"] += e["dir"] * e["vel"]
        if e["x"] < e["min_x"] or e["x"] > e["max_x"]:
            e["dir"] *= -1                                            # bate no limite e volta
        caixa_inimigo = pygame.Rect(int(e["x"]), int(e["y"]), e["w"], e["h"])
        if caixa.colliderect(caixa_inimigo):
            # caiu em cima (estava descendo e os pes estao na parte de cima do inimigo)?
            caiu_em_cima = (player.velocidade_y > 0 and
                            caixa.bottom <= caixa_inimigo.top + e["h"] // 2)
            if caiu_em_cima:
                e["vivo"] = False                                    # derrota o inimigo
                player.velocidade_y = -9                             # da um quique pra cima
            elif jogo["invuln_timer"] == 0:
                jogo["vidas"] -= 1
                jogo["invuln_timer"] = FPS                           # 1 segundo sem tomar dano
                if jogo["vidas"] <= 0:
                    return "GAMEOVER"

    # 8) venceu? chegou na bandeira com os carvoes necessarios
    if player.x >= BANDEIRA_X and jogo["contagem"]["carvao"] >= CARVOES_PARA_VENCER:
        return "VITORIA"

    # 9) camera: acompanha o Mario, sem passar das bordas do mapa
    cam = player.x + player.width / 2 - SCREEN_W / 2
    cam = max(0, min(cam, MAP_LARGURA - SCREEN_W))
    jogo["cam_x"] = cam

    return "JOGANDO"


# ------------------------------- DESENHO ------------------------------------

def desenhar_nuvem(tela, cx, cy):
    """Desenha uma nuvem simples com alguns circulos brancos."""
    branco = (255, 255, 255)
    pygame.draw.circle(tela, branco, (cx, cy), 18)
    pygame.draw.circle(tela, branco, (cx + 20, cy + 4), 14)
    pygame.draw.circle(tela, branco, (cx - 20, cy + 4), 14)
    pygame.draw.rect(tela, branco, (cx - 20, cy, 40, 12))


def desenhar_fundo(tela, cam_x):
    """Fundo tematico do Brasil: predios verde-amarelos, nuvens e bandeirinhas.
    Cada camada anda mais devagar que o jogo (parallax), dando sensacao de profundidade."""
    base_y = LINHA_CHAO * TILE

    # predios ao fundo (andam a metade da velocidade)
    desloc = int(cam_x * 0.5)
    largura_p = 96
    cores = [(96, 130, 96), (196, 176, 86), (110, 140, 110), (206, 190, 96)]
    for i in range(-1, SCREEN_W // largura_p + 2):
        x = i * largura_p - (desloc % largura_p)
        idx = (i + desloc // largura_p) % len(cores)
        altura_p = 100 + idx * 16
        pygame.draw.rect(tela, cores[idx], (x, base_y - altura_p, largura_p - 10, altura_p))
        for jy in range(base_y - altura_p + 14, base_y - 14, 26):     # janelinhas
            for jx in range(x + 12, x + largura_p - 20, 24):
                pygame.draw.rect(tela, (245, 240, 170), (jx, jy, 8, 12))

    # nuvens (andam bem devagar)
    desloc_n = int(cam_x * 0.25)
    for i in range(-1, SCREEN_W // 300 + 2):
        cx = i * 300 - (desloc_n % 300) + 100
        desenhar_nuvem(tela, cx, 80)
        desenhar_nuvem(tela, cx + 150, 150)

    # bandeirinhas verde e amarelo no topo da tela
    largura_b = 28
    for i in range(SCREEN_W // largura_b + 1):
        x = i * largura_b
        cor = (0, 150, 60) if i % 2 == 0 else (255, 210, 0)
        pygame.draw.polygon(tela, cor, [(x, 0), (x + largura_b, 0), (x + largura_b // 2, 20)])


def desenhar_mundo(tela, cam_x):
    """Desenha o ceu, o chao (com buracos), as plataformas e a escada."""
    # so desenha as colunas que estao na tela (mais rapido)
    col_ini = max(0, int(cam_x // TILE) - 1)
    col_fim = min(mapa.MAP_COLS, int((cam_x + SCREEN_W) // TILE) + 2)

    # chao
    for col in range(col_ini, col_fim):
        if not col_eh_buraco(col):
            for linha in range(LINHA_CHAO, mapa.MAP_ROWS):
                cor = mapa.COR_CHAO_TOP if linha == LINHA_CHAO else mapa.COR_CHAO
                pygame.draw.rect(tela, cor, (col * TILE - cam_x, linha * TILE, TILE, TILE))

    # plataformas
    for linha, c_inicio, c_fim in mapa.PLATAFORMAS:
        for col in range(c_inicio, c_fim + 1):
            x = col * TILE - cam_x
            if -TILE <= x <= SCREEN_W:
                pygame.draw.rect(tela, mapa.COR_PLAT, (x, linha * TILE, TILE, TILE))
                pygame.draw.rect(tela, mapa.COR_PLAT_TOP, (x, linha * TILE, TILE, 6))

    # escada
    for col, altura in mapa.ESCADA:
        for i in range(altura):
            linha = 13 - i
            x = col * TILE - cam_x
            if -TILE <= x <= SCREEN_W:
                pygame.draw.rect(tela, mapa.COR_CHAO, (x, linha * TILE, TILE, TILE))
                pygame.draw.rect(tela, mapa.COR_CHAO_TOP, (x, linha * TILE, TILE, 6))


def desenhar_bandeira(tela, cam_x):
    """Desenha a bandeira de chegada no fim do nivel."""
    x = BANDEIRA_X - cam_x
    if -TILE <= x <= SCREEN_W:
        topo = (BANDEIRA_LINHA - 4) * TILE
        base = (LINHA_CHAO) * TILE
        pygame.draw.rect(tela, (230, 230, 230), (x, topo, 4, base - topo))     # mastro
        pygame.draw.polygon(tela, (0, 160, 0),                                  # bandeirinha
                            [(x + 4, topo), (x + 4 + 26, topo + 10), (x + 4, topo + 20)])


def desenhar_coletaveis(tela, cam_x, coletaveis):
    """Desenha cada coletavel ainda nao pego, com a cor do seu tipo."""
    for c in coletaveis:
        if not c["coletado"]:
            x = c["rect"].x - cam_x
            if -TILE <= x <= SCREEN_W:
                centro = (int(x + 10), int(c["rect"].y + 10))
                pygame.draw.circle(tela, COR_DO_TIPO[c["tipo"]], centro, 11)
                pygame.draw.circle(tela, (0, 0, 0), centro, 11, 2)


def desenhar_inimigos(tela, cam_x, jogo):
    """Desenha os inimigos usando o sprite, virando conforme a direcao."""
    sprite = jogo["sprite_inimigo"]
    for e in jogo["inimigos"]:
        if not e["vivo"]:
            continue
        x = e["x"] - cam_x
        if -TILE <= x <= SCREEN_W:
            imagem = sprite if e["dir"] > 0 else pygame.transform.flip(sprite, True, False)
            tela.blit(imagem, (x, e["y"]))


def desenhar_hud(tela, fonte, jogo):
    """Desenha o painel de informacoes (vidas e contagem de coletaveis)."""
    linhas = [
        "Vidas: {}".format(jogo["vidas"]),
        "Carne: {}".format(jogo["contagem"]["carne"]),
        "Carvao: {}/{}".format(jogo["contagem"]["carvao"], CARVOES_PARA_VENCER),
        "Breja: {}".format(jogo["contagem"]["breja"]),
    ]
    y = 8
    for texto in linhas:
        img = fonte.render(texto, True, (0, 0, 0))
        tela.blit(img, (10, y))
        y += 24
    if jogo["boost_timer"] > 0:
        img = fonte.render("BOOST!", True, (200, 120, 0))
        tela.blit(img, (10, y))


def desenhar_jogo(tela, fonte, jogo):
    """Junta tudo: ceu, mundo, bandeira, coletaveis, inimigos, Mario e HUD."""
    cam_x = jogo["cam_x"]
    tela.fill(mapa.COR_CEU)
    desenhar_fundo(tela, cam_x)
    desenhar_mundo(tela, cam_x)
    desenhar_bandeira(tela, cam_x)
    desenhar_coletaveis(tela, cam_x, jogo["coletaveis"])
    desenhar_inimigos(tela, cam_x, jogo)

    # o Mario pisca enquanto esta invencivel (logo depois de tomar dano)
    player = jogo["player"]
    piscando = jogo["invuln_timer"] > 0 and (jogo["invuln_timer"] // 5) % 2 == 0
    if not piscando:
        tela.blit(player.image, (player.x - cam_x, player.y))

    desenhar_hud(tela, fonte, jogo)


def desenhar_texto_centro(tela, fonte, texto, cor, y):
    """Desenha um texto centralizado na horizontal."""
    img = fonte.render(texto, True, cor)
    tela.blit(img, (SCREEN_W // 2 - img.get_width() // 2, y))


def desenhar_menu(tela, fonte_grande, fonte):
    tela.fill(mapa.COR_CEU)
    desenhar_texto_centro(tela, fonte_grande, "Super Mario Carne", (0, 0, 0), 200)
    desenhar_texto_centro(tela, fonte, "Aperte ENTER para comecar", (0, 0, 0), 300)
    desenhar_texto_centro(tela, fonte, "Setas para andar, ESPACO para pular", (0, 0, 0), 340)


def desenhar_overlay(tela, fonte_grande, fonte, titulo, cor, subtitulo):
    """Escurece a tela e escreve uma mensagem (vitoria ou game over)."""
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

    estado = "MENU"                 # MENU, JOGANDO, VITORIA ou GAMEOVER
    jogo = novo_jogo()

    rodando = True
    while rodando:
        # ---- PASSO 1: ler eventos ----
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                if estado in ("MENU", "VITORIA", "GAMEOVER"):
                    jogo = novo_jogo()
                    estado = "JOGANDO"

        # ---- PASSOS 2 a 4: logica (so quando esta jogando) ----
        if estado == "JOGANDO":
            estado = atualizar_playing(jogo)

        # ---- PASSO 5: desenhar tudo ----
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

        # ---- PASSO 6: mostrar na tela ----
        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()