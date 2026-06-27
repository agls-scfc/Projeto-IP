import pygame
import sys

# ============================================================
#  CONFIGURAÇÕES
# ============================================================
TILE      = 32
SCREEN_W  = 800
SCREEN_H  = 600
FPS       = 60

COR_CEU       = (135, 206, 235)
COR_CHAO      = (139,  69,  19)
COR_CHAO_TOP  = (160,  82,  45)
COR_PLAT      = ( 34, 139,  34)
COR_PLAT_TOP  = ( 50, 205,  50)
COR_JOGADOR   = (220,  20,  60)

# ============================================================S

MAP_COLS = 170
MAP_ROWS = 18

BURACOS = [
    (22, 25),    # Seção 2 — buraco pequeno
    (32, 38),    # Seção 2 — buraco médio
    (45, 56),    # Seção 3 — pit grande (use as plataformas para atravessar)
    (68, 72),    # Seção 4
    (80, 83),    # Seção 4
    (97, 100),   # Seção 5
    (108, 113),  # Seção 6
    (120, 123),  # Seção 6
    (133, 137),  # Seção 7
    (143, 148),  # Seção 7
    (155, 159),  # Seção 7 — último grande buraco
]

COLETAVEIS = [
    # (linha, coluna) — placeholder, sem lógica ainda
    # Seção 2
    (11, 23), (11, 24),   # antes do 1º buraco
    ( 8, 29),   # acima da plataforma elevada
    # Seção 3 — guiam o caminho pelo pit
    ( 9, 47), ( 7, 52), ( 9, 57),
    # Seção 4
    (10, 65), (10, 66),
    # Seção 5
    ( 8, 92), ( 8, 93),   # topo da escada
    # Seção 6
    (10, 116), (10, 117),
    # Seção 7
    ( 7, 141), ( 7, 142), # coletável alto
    (11, 152),
    # Seção 8
    (11, 163),
]

PLATAFORMAS = [
    # (linha, col_inicio, col_fim)

    # --- Seção 2: Aquecimento ---
    (11, 28, 30),   # plataforma elevada
    (9, 33, 35),   # sobre 2º buraco

    # --- Seção 3: Pit Grande ---
    (12, 46, 48),
    (10, 51, 53),   # plataforma mais alta no meio
    (12, 56, 58),

    # --- Seção 4: Zona de Inimigos (sem inimigos ainda) ---
    (11, 64, 67),   
    (12, 75, 78),   # sobre buraco

    # --- Seção 5: Escadaria ---
    (12, 91, 93),
    (10, 97, 99),   # topo da escada, sobre buraco

    # --- Seção 6: Gauntlet ---
    (12, 105, 107),
    (13, 108, 113), # sobre buraco largo
    (11, 115, 118),
    (13, 120, 123), # sobre buraco

    # --- Seção 7: Saltos Finais ---
    (12, 128, 131),
    (10, 133, 136), # alto, sobre buraco
    ( 9, 140, 143), # ainda mais alto
    (12, 143, 148), # sobre buraco largo
    (10, 151, 154),
    (12, 155, 159), # sobre último buraco

    # --- Seção 8: Chegada ---
    (12, 162, 164),
]
