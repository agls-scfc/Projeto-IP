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
 
MAP_COLS = 170
MAP_ROWS = 18
 
BURACOS = [
    (22, 25),    # Seção 2 — buraco pequeno
    (32, 38),    # Seção 2 — buraco médio    
    (68, 72),    # Seção 4
    (80, 83),    # Seção 4
    (97, 100),   # Seção 5
    (108, 113),  # Seção 6
    (120, 123),  # Seção 6
    (133, 137),  # Seção 7
    (143, 148),  # Seção 7
    (155, 159),  # Seção 7 — último grande buraco
]
 
INIMIGOS = [
    # (linha, coluna) — placeholder, sem lógica ainda
    # Linha 13 = em cima do chão | outras linhas = em cima de plataforma
    (13, 15),   # Seção 1 — primeiro inimigo
    (13, 28),   # Seção 2
    (13, 52),   # Seção 4
    (13, 76),   # Seção 4
    (13, 85),   # Seção 5
    (10, 95),   # Seção 5 — topo da escada
    (13, 104),  # Seção 6
    (13, 119),  # Seção 6
    (13, 125),  # Seção 7
    (13, 130),  # Seção 7
    ( 9, 141),  # Seção 7 — alto
    (13, 152),  # Seção 7
    (13, 161),  # Seção 8 — último inimigo
]
 
COLETAVEIS = [
    # (linha, coluna) — placeholder, sem lógica ainda
    # Seção 2
    (11, 23), (11, 24),   # antes do 1º buraco
    # Seção 3 — guiam o caminho pelo pit
    ( 9, 47), ( 9, 52), ( 9, 57),
    # Seção 4
    (10, 65), (10, 66),
    # Seção 5
    ( 8, 92),   # topo da escada
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
    (11, 28, 29),   # plataforma elevada
    (9, 34, 36),   # sobre 2º buraco
 
    # --- Seção 3: Pit Grande ---
    (12, 46, 48),
    (8, 51, 53),   # plataforma mais alta no meio
    (12, 56, 58),
 
    # --- Seção 4: Zona de Inimigos (sem inimigos ainda) ---
    (11, 64, 67),   
    (12, 75, 77),   # sobre buraco
 
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
