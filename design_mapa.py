import pygame
import sys

TILE      = 32
SCREEN_W  = 800
SCREEN_H  = 576
FPS       = 60
# Essas cores eu deixei só pra testar o mapa
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


MAP_COLS = 220
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

    # --- EXTENSÃO (seções 9-11) ---
    (170, 174),
    (181, 187),
    (194, 200),
    (207, 212),
]

PLATAFORMAS = [
    # (linha, col_inicio, col_fim)

    (12,  16,  18),
    (11,  29,  31),
    (11,  35,  36),
    (12,  45,  47),
    (11,  54,  55),
    (11,  62,  64),
    (12,  71,  72),
    (12,  88,  90),
    (11,  92,  93),
    (10,  95,  97),
    (12, 105, 107),
    (11, 111, 114),
    (12, 118, 120),
    (12, 129, 131),
    (10, 134, 137),
    (11, 147, 147),
    (12, 152, 154),
    (10, 157, 159),
    (12, 163, 165),
    (11, 183, 185),
    (11, 196, 198),
    (12, 202, 203),
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

    (13, 167),
    (13, 178),
    (10, 184),
    (13, 191),
    (10, 197),
    (13, 203),
    (13, 215),
]

COLETAVEIS = [
    # --- Carvão ---
    ( 5, 100, "carvao"),
    ( 8, 184, "carvao"),
    ( 8, 205, "carvao"),

    # --- Breja ---
    ( 9, 135, "breja"),
    ( 9, 197, "breja"),

    # --- Carne ---
    (11,  46, "carne"),
    (11, 164, "carne"),
]
