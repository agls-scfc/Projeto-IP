# Super Mario Carne 🥩🇧🇷

Jogo de plataforma 2D inspirado no *Super Mario Bros.* clássico, com a temática do Brasil em clima de Copa do Mundo (o "Rumo ao Hexa") e de churrasco. Desenvolvido em Python com a biblioteca Pygame, como projeto da disciplina de Introdução à Programação.

> **Sobre este documento:** este README registra a ideia e as regras do jogo e vai crescendo ao longo do projeto até virar o relatório final exigido pela disciplina (arquitetura, bibliotecas, divisão de tarefas, desafios e lições). As seções marcadas com *a preencher* serão completadas conforme o projeto avança.

---

## Equipe

- Arthur Salazar
- Eduardo Cabral
- João Pedro Santos
- Pedro Henrique Cavalcanti
- Rafael Salles
- Rafael Vitor

---

## Conceito do jogo

O jogador controla o Mario num único nível grande e horizontal, num cenário brasileiro: prédios verde-amarelos, faixa de "Rumo ao Hexa", bandeira do Brasil, estádio ao fundo e churrasqueiras espalhadas pelo caminho. O objetivo é atravessar o nível coletando itens, desviando dos inimigos e dos buracos, e chegando ao final com os 5 carvões necessários para "acender a churrasqueira" e vencer.

Durante a partida, o jogo mantém e exibe na tela a contagem de cada tipo de coletável (requisito da disciplina).

---

## Como jogar

**Objetivo:** chegar ao fim do nível tendo coletado os 5 carvões, sobrevivendo aos inimigos e aos buracos do mapa.

**Controles:**

| Tecla | Ação |
|-------|------|
| ← / → | Andar para a esquerda / direita |
| Espaço | Pular |

---

## Coletáveis

O jogo tem **três tipos** de coletáveis, cada um com um efeito diferente. A quantidade coletada de cada tipo é mostrada na tela durante a partida.

| Coletável | Efeito |
|-----------|--------|
| 🥩 **Carne** | Recupera 1 vida do Mario, até o máximo de 3 vidas. |
| 🪨 **Carvão** | Item-objetivo: é preciso coletar **5 carvões** para conseguir terminar o nível com sucesso. |
| 🍺 **Cerveja** | *Boost* que aumenta a velocidade do Mario por **5 segundos**. |

---

## Mecânicas

**Vidas.** O Mario começa com **3 vidas** e esse é também o limite máximo. Ele **recupera** vida coletando carne (sem passar de 3) e **perde** vida ao:

- encostar num inimigo, ou
- cair em um buraco do mapa.

**Queda no mapa.** Cair em um buraco custa 1 vida e faz o Mario voltar ao início do nível.

**Vitória.** Acontece quando o Mario chega ao final do nível tendo coletado os 5 carvões.

**Derrota (game over).** Acontece quando as 3 vidas chegam a zero.

---

## Fluxo do jogo

A "main" (laço principal) controla a passagem entre os estados do jogo:

1. **Menu inicial** → o jogador aperta uma tecla para começar.
2. **Jogando** → o laço principal roda: lê comandos, move tudo, checa colisões, conta coletáveis e desenha a tela.
3. A partir do "Jogando", o jogo pode ir para:
   - **Vitória** → chegou ao fim com os 5 carvões.
   - **Game over** → as vidas acabaram.
4. Das telas de vitória / game over → o jogador pode reiniciar ou sair.

*(Um diagrama visual desse fluxo pode ser adicionado aqui depois.)*

---

## Detalhes de implementação

- **Câmera:** como o nível é maior que a tela, a câmera acompanha o Mario conforme ele avança. O cenário de fundo é único (pode ser incrementado depois).
- **Pontuação:** não há um sistema de pontos separado; a contagem de coletáveis exibida na tela cumpre o registro exigido pela disciplina.

### Ainda em definição

Pontos que a equipe ainda vai fechar:

1. **Inimigos:** se será possível derrotá-los pulando na cabeça (estilo Mario) ou apenas desviar. Em ambos os casos, encostar de lado custa uma vida.
2. **Carvão insuficiente no fim:** o que acontece se o Mario chegar ao final sem os 5 carvões (proposta atual: a churrasqueira final não acende e o jogador precisa voltar para coletar o que falta).

---

## Como rodar

```bash
pip install pygame
python main.py
```

*(Instruções detalhadas a preencher quando o jogo estiver rodando.)*

---

## Arquitetura do projeto

*A preencher conforme o código for escrito.* Visão geral planejada:

- `main.py` — laço principal do jogo (game loop): cria os objetos, lê comandos, atualiza o estado, checa colisões, conta coletáveis e desenha tudo na tela.
- `src/entities/` — classes dos elementos do jogo:
  - `player.py` — o Mario (movimento, pulo, vidas).
  - `enemy.py` — os inimigos.
  - `collectibles.py` — os coletáveis (carne, carvão, cerveja).
- `src/images/` — imagens (sprites) usadas no jogo.

---

## Tecnologias utilizadas

- **Python** — linguagem exigida pela disciplina.
- **Pygame** — biblioteca para criação de jogos 2D em Python. *(Justificativa a detalhar no relatório: facilita o desenho na tela, a captura do teclado e a detecção de colisões, sendo a ferramenta tradicionalmente usada nesses projetos.)*

---

## Divisão de tarefas

*A preencher pela equipe (o relatório exige indicar quem fez o quê).*

| Integrante | Responsabilidade |
|------------|------------------|
| Rafael Vitor | `main.py` / lógica e laço principal do jogo |
| *(preencher)* | Personagem / Mario |
| *(preencher)* | Coletáveis |
| *(preencher)* | Inimigos |
| *(preencher)* | Cenário / arte |
| *(preencher)* | ... |

---

## Galeria

*Capturas de tela do jogo funcionando — a preencher.*

---

## Relatório: desafios e lições

*A preencher ao final do projeto (perguntas exigidas pela disciplina):*

- Qual foi o maior erro cometido durante o projeto? Como lidaram com ele?
- Qual foi o maior desafio enfrentado? Como lidaram com ele?
- Quais as lições aprendidas?