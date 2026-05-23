# 🚀 Space Shooter: Skills Edition — SENAI-SP · IA com Google Antigravity

> **Arcade space shooter estilo Atari** desenvolvido em Python com Pygame — nave reativa, dash duplo, power-ups, asteroides progressivos e efeitos visuais de partículas.
>
> Atividade prática do curso **IA com Google Antigravity** no SENAI-SP.

---

## 🎮 Sobre o Jogo

**Space Shooter: Skills Edition** é um jogo 2D de tiro espacial inspirado nos clássicos arcades Atari. O jogador controla uma nave e deve sobreviver a ondas crescentes de asteroides, coletando power-ups e acumulando pontuação enquanto o desafio escala progressivamente.

---

## ✨ Funcionalidades

### 🛸 Nave do Jogador
- Movimentação lateral fluida com inclinação dinâmica da sprite
- **Mecânica de Dash** — duplo toque rápido (`←←` ou `→→` em até 250ms) executa um dash explosivo com cooldown
- Efeito de **propulsor com partículas** animadas em tempo real
- Piscar de invencibilidade temporária ao ser atingido

### 🔫 Sistema de Tiro

| Tipo   | Descrição                          |
|--------|------------------------------------|
| Normal | 1 projétil reto                    |
| Triple | 3 projéteis paralelos (azul)       |
| Spread | 3 projéteis em leque de 25° (roxo) |

### ☄️ Asteroides com Dificuldade Progressiva
- Velocidade e taxa de spawn aumentam com a pontuação
- Velocidade inicial: `1.5` → máximo: `7.0` (cresce `+0.15` por ponto)
- Spawn inicial a cada `90 frames` → mínimo de `20 frames`

### ⚡ Power-ups

| Power-up    | Efeito                    | Duração    |
|-------------|---------------------------|------------|
| Triple Shot | 3 tiros paralelos         | ~8s        |
| Spread Shot | 3 tiros em leque          | ~8s        |
| Life        | +1 vida (máx. 5)          | Permanente |

> 15% de chance de drop ao destruir um asteroide.

### 🌟 Efeitos Visuais
- **Fundo estrelado** com 120 estrelas cintilantes animadas
- **Screen shake** ao colidir ou explodir asteroides
- **Partículas de explosão** coloridas com física de desaceleração
- **Partículas de propulsor** na cauda da nave
- **Popups de score** flutuantes ao destruir inimigos
- **HUD** com barra de power-up e vidas representadas visualmente

---

## 🗂️ Estrutura do Projeto

```
jogo-atari/
├── settings.py      # Constantes e configurações globais
├── game.py          # Loop principal, HUD, partículas, colisões
├── player.py        # Classe da nave, dash, tiro, efeitos
├── bullet.py        # Projéteis (normal, triple, spread)
├── asteroid.py      # Asteroides com dificuldade progressiva
├── powerup.py       # Power-ups com drop aleatório
└── README.md
```

---

## 🛠️ Tecnologias

- **Python 3.x**
- **Pygame** — motor gráfico, eventos, colisões e som

---

## ▶️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/ThurSilveira/jogo-atari.git
cd jogo-atari
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install pygame
```

### 4. Execute o jogo

```bash
python game.py
```

---

## 🎯 Controles

| Tecla                         | Ação                    |
|-------------------------------|-------------------------|
| `←` / `→`                    | Mover nave              |
| `←←` / `→→` _(duplo toque)_ | **Dash** lateral        |
| `SPACE`                       | Atirar                  |
| `R`                           | Reiniciar _(Game Over)_ |
| `ESC`                         | Sair do jogo            |

---

## 📸 Gameplay

```
⭐ Space Shooter: Skills Edition ⭐
┌──────────────────────────────┐
│  Score: 42          ♥ ♥ ♥   │
│  [══════░░░░] triple shot    │
│                              │
│        ☆  ✦  ★  ✦           │
│              ▲               │  ← Nave
│   ☄  ☄            ☄  ☄     │  ← Asteroides
└──────────────────────────────┘
```

---

## 👨‍💻 Autor

**Arthur Silveira** — [@ThurSilveira](https://github.com/ThurSilveira)

---

## 📄 Licença

Projeto de uso educacional — SENAI-SP · Curso IA com Google Antigravity.
