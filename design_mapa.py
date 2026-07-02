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
#  PLATAFORMAS: (linha, coluna_inicio, coluna_fim)
#  INIMIGOS:    (linha, coluna)
#  COLETAVEIS:  (linha, coluna, cor)
#  ESCADA:      (coluna, altura)  -> blocos sólidos empilhados sobre o chão
#  BANDEIRA:    (linha_base, coluna)


MAP_COLS = 245
MAP_ROWS = 18

BURACOS = [
    ( 24,  27),
    ( 33,  38),
    ( 52,  57),
    ( 70,  73),
    ( 82,  85),
    ( 98, 101),
    (110, 115),
    (122, 125),
    (134, 138),
    (145, 150),
    (156, 160),
    (170, 174),
    (181, 187),
    (194, 200),
    (207, 212),
]

PLATAFORMAS = [
    # (linha, col_inicio, col_fim)

    (11,  16,  18),
    (11,  29,  31),
    (11,  35,  36),
    (11,  45,  47),
    (11,  54,  55),
    (11,  62,  64),
    (11,  71,  72),
    (11,  88,  90),
    (11,  92,  93),
    (10,  95,  97),
    (11, 105, 107),
    (11, 112, 113),
    (11, 118, 120),
    (11, 129, 131),
    (10, 135, 136),
    (11, 147, 147),
    (11, 152, 154),
    (10, 157, 159),
    (11, 163, 165),
    (11, 183, 185),
    (11, 196, 198),
    (10, 204, 205),
    (11, 208, 211),
    (11, 216, 218),
]

INIMIGOS = [
    # (linha, coluna)
    # Linha 13 = sobre o chão | (linha_plataforma - 1) = sobre plataforma
    (13,  12),
    (13,  30),
    (13,  44),
    (13,  63),
    (13,  78),
    (13,  90),
    ( 9,  96),
    (13, 106),
    (11, 119),
    (13, 130),
    (13, 142),
    (11, 153),
    # --- EXTENSÃO ---
    (13, 167),
    (13, 178),
    (10, 184),
    (13, 191),
    (10, 197),
    (13, 203),
    (13, 215),
]

COLETAVEIS = [
    # --- carvao ---
    ( 5, 100, "amarela"),
    ( 8, 184, "amarela"),
    ( 8, 205, "amarela"),

    # --- carne ---
    ( 9, 135, "vermelha"),
    ( 9, 197, "vermelha"),

    # --- breja ---
    (11,  46, "azul"),
    (11, 164, "azul"),
]

ESCADA = [
    (228, 1),
    (229, 2),
    (230, 3),
    (231, 4),
    (232, 5),
    (233, 6),
    (234, 6),
]
# Bandeira de chegada (placeholder, sem função ainda).
BANDEIRA = (13, 240)
