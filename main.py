#  SUPER MARIO CARNE 


import pygame
import design_mapa as mapa                      
from src.entities.player import Player          


# ------------------------- CONSTANTES DO JOGO -------------------------------

TILE       = mapa.TILE                          
SCREEN_W   = mapa.SCREEN_W                       
SCREEN_H   = mapa.SCREEN_H                       
FPS        = mapa.FPS                            

LINHA_CHAO = 14                                  
MAP_LARGURA = mapa.MAP_COLS * TILE               

MORTE_QUEDA_Y = 480

INICIO_X = 2 * TILE
INICIO_Y = LINHA_CHAO * TILE - 45                 

BANDEIRA_LINHA, BANDEIRA_COL = mapa.BANDEIRA
BANDEIRA_X = BANDEIRA_COL * TILE

COR_CARNE  = (200,  40,  40)                       
COR_CARVAO = ( 60,  60,  60)                       
COR_BREJA  = (230, 180,  40)                       

TIPO_POR_COR = {"vermelha": "carne", "amarela": "carvao", "azul": "breja"}
COR_DO_TIPO  = {"carne": COR_CARNE, "carvao": COR_CARVAO, "breja": COR_BREJA}


# ------------------- CONSTRUCAO DO MUNDO ------------------

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
    lista = []
    for linha, col, cor in mapa.COLETAVEIS:
        tipo = TIPO_POR_COR.get(cor, "carvao")
        rect = pygame.Rect(col * TILE + 6, linha * TILE + 6, 20, 20)
        lista.append({"rect": rect, "tipo": tipo, "coletado": False})
    return lista

def criar_player():
    p = Player(INICIO_X, INICIO_Y)
    p.y = LINHA_CHAO * TILE - p.height
    return p

def novo_jogo():

    return {
        "player": criar_player(),
        "solidos": construir_solidos(),
        "coletaveis": construir_coletaveis(),
        "cam_x": 0,                
    }


# ------------------------------- LOGICA -------------------------------------

def rect_do_player(player):
    return pygame.Rect(int(player.x), int(player.y), player.width, player.height)

def resolver_colisao_vertical(player, solidos):
    player.no_chao = False
    caixa = rect_do_player(player)
    for s in solidos:
        if caixa.colliderect(s):
            if player.velocidade_y > 0:            
                player.y = s.top - player.height
                player.velocidade_y = 0
                player.no_chao = True
            elif player.velocidade_y < 0:          
                player.y = s.bottom
                player.velocidade_y = 0
            caixa = rect_do_player(player)

def voltar_ao_inicio(player):
    player.x = INICIO_X
    player.y = LINHA_CHAO * TILE - player.height
    player.velocidade_y = 0

def atualizar_playing(jogo):
    player = jogo["player"]

    # Movimento e colisão básica
    player.update()
    resolver_colisao_vertical(player, jogo["solidos"])

    if player.x < 0:
        player.x = 0
    if player.x > MAP_LARGURA - player.width:
        player.x = MAP_LARGURA - player.width

    # Caiu no buraco (Ainda sem sistema de vidas)
    if player.y > MORTE_QUEDA_Y:
        voltar_ao_inicio(player)

    caixa = rect_do_player(player)

    # Coleta básica (apenas visual por enquanto)
    for c in jogo["coletaveis"]:
        if not c["coletado"] and caixa.colliderect(c["rect"]):
            c["coletado"] = True
            print(f"Pegou: {c['tipo']} (Lógica de pontuação pendente)")

    # Câmera acompanha
    cam = player.x + player.width / 2 - SCREEN_W / 2
    cam = max(0, min(cam, MAP_LARGURA - SCREEN_W))
    jogo["cam_x"] = cam


# ------------------------------- DESENHO ------------------------------------

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
        base = (LINHA_CHAO) * TILE
        pygame.draw.rect(tela, (230, 230, 230), (x, topo, 4, base - topo))     
        pygame.draw.polygon(tela, (0, 160, 0),                                  
                            [(x + 4, topo), (x + 4 + 26, topo + 10), (x + 4, topo + 20)])

def desenhar_coletaveis(tela, cam_x, coletaveis):
    for c in coletaveis:
        if not c["coletado"]:
            x = c["rect"].x - cam_x
            if -TILE <= x <= SCREEN_W:
                centro = (int(x + 10), int(c["rect"].y + 10))
                pygame.draw.circle(tela, COR_DO_TIPO[c["tipo"]], centro, 11)
                pygame.draw.circle(tela, (0, 0, 0), centro, 11, 2)

def desenhar_jogo(tela, jogo):
    cam_x = jogo["cam_x"]
    tela.fill(mapa.COR_CEU)
    desenhar_mundo(tela, cam_x)
    desenhar_bandeira(tela, cam_x)
    desenhar_coletaveis(tela, cam_x, jogo["coletaveis"])
    
    player = jogo["player"]
    tela.blit(player.image, (player.x - cam_x, player.y))


# ------------------------------- LACO PRINCIPAL -----------------------------

def main():
    pygame.init()
    tela = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Super Mario Carne - WIP")
    relogio = pygame.time.Clock()

    jogo = novo_jogo()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        atualizar_playing(jogo)
        desenhar_jogo(tela, jogo)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()