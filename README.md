# Super Mario Carne 🥩🇧🇷

Jogo de plataforma 2D inspirado no *Super Mario Bros.* clássico, com a temática do Brasil em clima de Copa do Mundo e de churrasco. Desenvolvido em Python com a biblioteca Pygame, como projeto da disciplina de Introdução à Programação.

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

**Objetivo:** chegar ao fim do nível tendo coletado os 6 carvões, sobrevivendo aos inimigos e aos buracos do mapa.

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

**Vitória.** Acontece quando o Mario chega ao final do nível tendo coletado os 6 carvões.

**Derrota (game over).** Acontece quando as 3 vidas chegam a zero.

---

## Fluxo do jogo

A "main" (laço principal) controla a passagem entre os estados do jogo:

1. **Menu inicial** → o jogador aperta uma tecla para começar.
2. **Jogando** → o laço principal roda: lê comandos, move tudo, checa colisões, conta coletáveis e desenha a tela.
3. A partir do "Jogando", o jogo pode ir para:
   - **Vitória** → chegou ao fim com os 6 carvões.
   - **Game over** → as vidas acabaram.
4. Das telas de vitória / game over → o jogador pode reiniciar ou sair.

---

## Como rodar

```bash
pip install pygame-ce
python main.py
```

---

## Arquitetura do projeto

```
Projeto-IP/
├── main.py        — ponto de entrada; inicia e roda o jogo
├── README.md
├── .gitignore
└── src/           — todo o conteúdo do jogo
    ├── script/    — arquivos de código
    │   ├── collectibles.py  — os coletáveis (carne, carvão, cerveja)
    │   ├── design_mapa.py   — definição do mapa e posição dos elementos
    │   ├── enemy.py         — os inimigos
    │   └── player.py        — o Mario (movimento, pulo, vidas)
    ├── images/    — sprites e imagens usadas no jogo
    └── musica/    — trilha sonora do jogo
```

`main.py` é o ponto de entrada: cria os objetos, lê os comandos do teclado, atualiza o estado do jogo, checa colisões, conta coletáveis e desenha tudo na tela a cada frame.

---

## Tecnologias utilizadas

| Ferramenta | Uso | Justificativa |
|------------|-----|---------------|
| **Python** | Linguagem principal | Exigida pela disciplina |
| **Pygame-CE** | Motor do jogo 2D | Facilita o desenho na tela, a captura do teclado e a detecção de colisões; é a biblioteca mais usada para esse tipo de projeto em Python. A edição Community (CE) foi adotada por oferecer suporte ao Python 3.14, versão utilizada pela equipe. |
| **Gemini** | Geração de imagens e música | Utilizado para criar os sprites, ilustrações e a trilha sonora do jogo, agilizando a produção de assets sem exigir habilidades manuais de design ou composição musical. |
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

Após definir a temática e as funcionalidades principais do jogo, a equipe buscou modularizar o desenvolvimento ao máximo, com cada membro responsável por sua parte. A comunicação foi feita principalmente pelo grupo de WhatsApp, para notificar problemas e avanços e manter o alinhamento sobre o andamento do projeto. Ao longo do processo, diversas mudanças tiveram que ser feitas e escolhas de design repensadas; comumente trocávamos ideias e possibilidades para decidir o produto final. Utilizamos diversas enquetes entre o grupo para tomar essas decisões com a ciência e consentimento de todos.

---

## Conceitos da disciplina utilizados no projeto

Ao longo do semestre, fizemos 6 listas de questões em Python, cada uma com um assunto. Todos esses conceitos foram aplicados diretamente no projeto:

**Lista 1. Comandos condicionais** — usados extensivamente no `main.py` para controlar os estados do jogo (jogando, vitória, game over), verificar colisões e checar se o jogador coletou os 6 carvões necessários para vencer. Também presentes em `player.py` para tratar eventos de teclado e em `collectibles.py` para identificar o tipo de coletável coletado.

**Lista 2. Laços de repetição** — o game loop principal em `main.py` é um laço `while` que roda a cada frame do jogo, atualizando todos os elementos da tela. Laços `for` são usados para iterar sobre listas de coletáveis, inimigos e plataformas definidas em `design_mapa.py`.

**Lista 3. Listas** — utilizadas em `design_mapa.py` para armazenar as posições de todos os elementos do mapa: buracos, plataformas, inimigos e coletáveis. O `main.py` percorre essas listas para instanciar os objetos do jogo.

**Lista 4. Funções** — o código é organizado em funções tanto no `main.py` (ex: `carregar_imagens()`, `main()`) quanto nos arquivos de entidades, separando responsabilidades e evitando repetição de código.

**Lista 5. Recursão** — aplicada em situações de lógica de jogo que envolvem verificações encadeadas, como o tratamento de estados consecutivos do personagem.

**Lista 6. Tuplas e dicionários** — as cores do cenário em `design_mapa.py` são definidas como tuplas RGB (ex: `COR_CHAO = (101, 67, 33)`). Dicionários são usados no `main.py` para organizar e acessar as imagens carregadas (`IMAGENS["carne"]`, `IMAGENS["carvao"]`, etc.).

**Orientação a Objetos (POO)** — pilar central do projeto. Implementamos uma hierarquia de classes em `collectibles.py`: a classe base `Collectible` (que herda de `pygame.sprite.Sprite`) define o comportamento comum a todos os coletáveis, e as subclasses `Carne`, `Carvao` e `Cerveja` herdam dela e implementam seus efeitos específicos via o método `aplicar_efeito()`. O mesmo padrão é seguido em `player.py` e `enemy.py`.

---

## Galeria

**Início da fase**

![Início da fase](src/images/prints%20do%20jogo/screenshot1.png)

**Boost de cerveja ativo**

![Boost de cerveja ativo](src/images/prints%20do%20jogo/screenshot2.png)

**Tela de vitória**

![Tela de vitória](src/images/prints%20do%20jogo/screenshot3.png)

**Game Over**

![Game Over](src/images/prints%20do%20jogo/screenshot4.png)

---

## Relatório: desafios e lições

Por sermos todos iniciantes, os desafios foram muitos e os erros abundantes.

**Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?**

O maior erro foi não ter usado uma plataforma de gerenciamento de tarefas, isso acarretou em muitos erros de implementação que custaram tempo para ser consertados. Não estávamos suficientemente cientes de como as partes dos outros participantes funcionavam e como elas interagiam entre si. Lidamos com o problema através de comunicação constante pelo WhatsApp e reuniões para alinhar o andamento de cada parte.

**Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?**

Aprender à utilizar versionamento de código ao mesmo tempo que aprendíamos sobre POO e pygame. Demoramos a ter segurança nos comandos que executávamos no terminal e entender como eles alterariam o funcionamento do nosso código, especialmente por estarmos lidando com uma parte da linguagem Python que não conheciamos. Superamos isso com pesquisa, tentativa e erro, e apoio mútuo entre os integrantes.

**Quais as lições aprendidas durante o projeto?**

Aprendemos como é participar de um projeto coletivo de verdade, como é trabalhar com códigos de outras pessoas e como funciona a criação de um jogo. Aprendemos principalmente quais erros não podemos cometer em projetos como esse. Logo, conquistamos conhecimentos que serão úteis para toda a nossa carreira. Hard skills (bibliotecas, POO, versionamento) e soft skills (organização, gerenciamento de tarefas).