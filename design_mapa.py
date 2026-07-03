import pygame
import sys

TILE      = 32
SCREEN_W  = 800
SCREEN_H  = 576
FPS       = 60

COR_CEU       = (135, 206, 235)
COR_CHAO      = (139,  69,  19)
COR_CHAO_TOP  = (160,  82,  45)
COR_PLAT      = ( 34, 139,  34)
COR_PLAT_TOP  = ( 50, 205,  50)
COR_JOGADOR   = (220,  20,  60)

#  BURACOS:     (coluna_inicio, coluna_fim)
#  PLATAFORMAS: (linha, coluna_inicio, coluna_fim)  -> so nas linhas 9, 10 ou 11
#  INIMIGOS:    (linha, coluna)                      -> linha 13 = sobre o chao
#  COLETAVEIS:  (linha, coluna, cor)                 -> amarela=carvao, vermelha=carne, azul=breja
#  ESCADA:      (coluna, altura)
#  BANDEIRA:    (linha_base, coluna)

MAP_COLS = 160
MAP_ROWS = 18

# Buracos no chao (largura no maximo 4, faceis de pular)
BURACOS = [
    ( 26,  28),
    ( 44,  46),
    ( 62,  65),
    ( 80,  82),
    ( 98, 101),
    (116, 118),
    (132, 135),
]

# Plataformas SO nas linhas 9, 10 e 11 (nunca 12/13), para o Mario de 60px
# caber por baixo (vao minimo de 64px) e ainda alcancar com o pulo.
PLATAFORMAS = [
    (11,  15,  17),
    (10,  31,  33),
    (11,  38,  40),
    (10,  52,  54),
    ( 9,  58,  60),
    (11,  68,  70),
    (10,  74,  76),
    (11,  88,  90),
    (10,  92,  94),
    ( 9, 104, 106),
    (11, 110, 112),
    (10, 122, 124),
    (11, 128, 130),
    ( 9, 140, 142),
    (10, 146, 148),
    (11, 152, 154),
]

# Inimigos, todos sobre o chao (linha 13), longe dos buracos
INIMIGOS = [
    (13,  12),
    (13,  32),
    (13,  50),
    (13,  72),
    (13,  90),
    (13, 104),
    (13, 112),
    (13, 126),
    (13, 144),
]

# Coletaveis: 6 carvao, 4 carne, 4 breja (todos alcancaveis)
COLETAVEIS = [
    # --- carvao (amarela) ---
    (13,  20, "amarela"),
    (10,  16, "amarela"),
    ( 9,  32, "amarela"),
    ( 8,  59, "amarela"),
    (10,  89, "amarela"),
    ( 8, 105, "amarela"),
    # --- carne (vermelha) ---
    (13,  36, "vermelha"),
    ( 9,  75, "vermelha"),
    (13, 108, "vermelha"),
    (10, 129, "vermelha"),
    # --- breja (azul) ---
    (13,  48, "azul"),
    (13,  84, "azul"),
    (10, 111, "azul"),
    ( 8, 141, "azul"),
]

# Sem escada (era so decorativa e atrapalhava). Fica a lista vazia.
ESCADA = []

# Bandeira de chegada, no chao perto do fim do nivel
BANDEIRA = (13, 156)