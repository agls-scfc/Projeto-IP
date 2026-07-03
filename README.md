# Super Mario Carne 🥩🇧🇷

Jogo de plataforma 2D inspirado no *Super Mario Bros.* clássico, com a temática do Brasil em clima de Copa do Mundo e de churrasco. Desenvolvido em Python com a biblioteca Pygame, como projeto da disciplina de Introdução à Programação.

> **Sobre este documento:** este README registra a ideia e as regras do jogo e vai crescendo ao longo do projeto até virar o relatório final exigido pela disciplina (arquitetura, bibliotecas, divisão de tarefas, desafios e lições). As seções marcadas com *a preencher* serão completadas conforme o projeto avança.

---

## Equipe

| Usuário | Nome |
|---------|------|
| agls | Arthur Salazar |
| eccs | Eduardo Cabral |
| jpmcs | João Pedro Santos |
| phrbc | Pedro Henrique Cavalcanti |
| rsm8 | Rafael Salles |
| rvsc2 | Rafael Vitor |

---

## Objetivos do projeto

- Criar um jogo divertido de jogar e de passar o tempo
- Celebrar a Copa do Mundo e a seleção brasileira
- Aprofundar conhecimentos sobre lógica de programação, gerenciamento de tarefas, plataformas de versionamento, bibliotecas em Python, entre outros
- Adquirir habilidades essenciais para um profissional na área de tecnologia

---

## Conceito do jogo

O jogador controla o Mario num único nível grande e horizontal, num cenário brasileiro: prédios verde-amarelos, faixa de "Rumo ao Hexa", bandeira do Brasil, estádio ao fundo e churrasqueiras espalhadas pelo caminho. O objetivo é atravessar o nível coletando itens, desviando dos inimigos e dos buracos, e chegando ao final com os 6 carvões necessários para "acender a churrasqueira" e vencer.

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
| 🪨 **Carvão** | Item-objetivo: é preciso coletar **6 carvões** para conseguir terminar o nível com sucesso. |
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

---

## Como rodar

```bash
pip install pygame-ce
python main.py
```

*(Instruções detalhadas a preencher quando o jogo estiver rodando.)*

---

## Arquitetura do projeto

O código está organizado dentro da pasta `src/`:

```
Projeto-IP/
├── main.py                  — laço principal do jogo
├── README.md
└── src/
    ├── entities/            — classes dos elementos do jogo
    │   ├── player.py        — o Mario (movimento, pulo, vidas)
    │   ├── enemy.py         — os inimigos
    │   └── collectibles.py  — os coletáveis (carne, carvão, cerveja)
    └── images/              — sprites e imagens usadas no jogo
```

`main.py` é o ponto de entrada: cria os objetos, lê os comandos do teclado, atualiza o estado do jogo, checa colisões, conta coletáveis e desenha tudo na tela a cada frame.

---

## Tecnologias utilizadas

| Ferramenta | Uso | Justificativa |
|------------|-----|---------------|
| **Python** | Linguagem principal | Exigida pela disciplina |
| **Pygame-CE** | Motor do jogo 2D | Facilita o desenho na tela, a captura do teclado e a detecção de colisões; é a biblioteca mais usada para esse tipo de projeto em Python. A edição Community (CE) foi adotada por oferecer suporte ao Python 3.14, versão utilizada pela equipe. |
| **VS Code** | IDE | Editor leve com bom suporte a Python e integração nativa com Git |
| **GitHub** | Hospedagem do código e documentação | Permite versionamento, histórico de mudanças e colaboração entre os membros da equipe |
| **Discord / WhatsApp** | Comunicação | Usados para reuniões, alinhamentos e notificação de avanços e problemas |

---

## Divisão de tarefas

| Integrante | Responsabilidade |
|------------|-----------------|
| Arthur Salazar | Coletáveis (`collectibles.py`) e slides de apresentação |
| Eduardo Cabral | Imagens, músicas e suas implementações |
| João Pedro Santos | Código do Player e dos inimigos |
| Pedro Henrique Cavalcanti | Criação do nível e alocação dos elementos no jogo |
| Rafael Salles | Implementação dos arquivos e funções na `main.py` |
| Rafael Vitor | Implementação dos arquivos e funções na `main.py` |

---

## Métodos de organização

Após definir a temática e as funcionalidades principais do jogo, a equipe buscou modularizar o desenvolvimento ao máximo, com cada membro responsável por sua parte. A comunicação foi feita principalmente pelo grupo de WhatsApp, para notificar problemas e avanços e manter o alinhamento sobre o andamento do projeto. Ao longo do processo, diversas mudanças tiveram que ser feitas e escolhas de design repensadas, comumente trocavamos ideias e possibilidades para decidir o produto final. Utilizamos diversas enquetes entre o grupo para tomar essas decisões com a ciência e conscentimento de todos.

---

## Galeria

*Capturas de tela do jogo funcionando — a preencher.*

---

## Relatório: desafios e lições

Por sermos todos iniciantes, os desafios foram muitos e os erros abundantes. Os principais foram:

**Erros enfrentados:**
- Erros de instalação (versões incompatíveis de Pygame e Python)
- Erros de Git e GitHub (commits mal organizados, má organização do repositório)

**Desafios enfrentados:**
- Falta de gerenciamento formal de tarefas (não utilizamos Notion, Trello, etc.)
- Aprender Orientação a Objetos do zero
- Debugar arquivos diferentes integrados entre si
- Entender como o Pygame funciona e como usar suas funções corretamente
