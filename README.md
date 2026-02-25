# Consulta Profissional de CNPJ

Um sistema *full-stack* desenvolvido para consultar dados de empresas através do CNPJ, consumindo a **BrasilAPI**. 

Este projeto foi construído com foco em **boas práticas de arquitetura**, separação de responsabilidades e tratamento de erros adequado, simulando um ambiente real de desenvolvimento corporativo.

## Tecnologias Utilizadas

**Frontend:**
* Vue.js 3
* Axios (para requisições HTTP)

**Backend:**
* Python 3
* Flask (Microframework web)
* Flask-CORS (Gerenciamento de permissões)
* Requests (Comunicação com a API externa)

**API Externa:**
* [BrasilAPI](https://brasilapi.com.br/) (Dados abertos do Brasil)

## ✨ Funcionalidades e Diferenciais Técnicos

* **Arquitetura Modular:** Backend estruturado utilizando *Blueprints* do Flask para escalabilidade e organização de rotas.
* **Validação e UX no Frontend:** Campo de input com aplicação de máscara automática (`00.000.000/0001-00`) utilizando Expressões Regulares (Regex) e bloqueio de caracteres inválidos.
* **Validação de Segurança (`utils`):** Sanitização e verificação do CNPJ no backend (garantindo 14 dígitos) antes de processar a requisição externa.
* **Tratamento de Exceções:** Retorno de *Status Codes* HTTP corretos (400, 404, 500) e mensagens de erro formatadas em JSON.
* **Interface Reativa:** Gerenciamento de estado (Loading) e exibição de alertas visuais caso o CNPJ não seja encontrado ou a API externa falhe.

## Estrutura do Projeto

O projeto adota uma separação clara entre cliente (Frontend) e servidor (Backend):

```text
projeto-cnpj/
├── backend/                  # API Rest (Python/Flask)
│   ├── app.py                # Ponto de entrada
│   ├── routes/               # Módulos de rotas (Blueprints)
│   ├── services/             # Regras de negócio e chamadas à BrasilAPI
│   └── utils/                # Funções auxiliares e validações
│
└── frontend/                 # Interface de Usuário (Vue.js)
    ├── src/
    │   ├── App.vue           # Componente principal de tela com a lógica
    │   └── services/         # Configuração do Axios
```

## Como executar o projeto localmente

### Pré-requisitos
* Node.js e npm instalados
* Python 3 instalado

### 1. Rodando o Backend (Flask)
Abra o terminal, navegue até a pasta `backend` e execute:

```bash
# Instale as dependências
pip install flask requests flask-cors

# Inicie o servidor
python app.py
```
O servidor iniciará na porta `http://localhost:5000`.

### 2. Rodando o Frontend (Vue.js)
Abra um **novo terminal**, navegue até a pasta `frontend` e execute:

```bash
# Instale as dependências do Node
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```
O aplicativo abrirá no seu navegador (geralmente em `http://localhost:5173`).

---
*Desenvolvido com dedicação e foco em Clean Code.* 💡

