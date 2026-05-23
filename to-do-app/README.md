# ✅ To-Do App — SENAI-SP · IA com Google Antigravity

> Aplicação full-stack de lista de tarefas desenvolvida como atividade prática do curso **IA com Google Antigravity** no SENAI-SP.

---

## 🧩 Stack

| Camada       | Tecnologia               |
|--------------|--------------------------|
| Frontend     | React + Vite             |
| Backend      | Node.js + Express        |
| Banco        | SQLite                   |
| Orquestração | Concurrently (mono-repo) |

---

## 🗂️ Estrutura do Projeto

```
to-do-app/
├── frontend/          # Aplicação React (Vite)
├── backend/           # API REST Express + SQLite
├── package.json       # Scripts de orquestração
└── README.md
```

---

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/ThurSilveira/jogo-atari.git
cd jogo-atari/to-do-app
```

### 2. Instale todas as dependências

```bash
npm run install:all
```

---

## ▶️ Executar em Desenvolvimento

```bash
npm start
```

Este comando sobe simultaneamente o backend e o frontend:

| Serviço  | URL padrão            |
|----------|-----------------------|
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:3000 |

---

## 📡 Endpoints da API

| Método | Rota         | Descrição                |
|--------|--------------|--------------------------|
| GET    | `/tasks`     | Lista todas as tarefas   |
| POST   | `/tasks`     | Cria uma nova tarefa     |
| PUT    | `/tasks/:id` | Atualiza uma tarefa      |
| DELETE | `/tasks/:id` | Remove uma tarefa        |

---

## 👨‍💻 Autor

**Arthur Silveira** — [@ThurSilveira](https://github.com/ThurSilveira)

---

## 📄 Licença

Projeto de uso educacional — SENAI-SP · Curso IA com Google Antigravity.
