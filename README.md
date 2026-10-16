# portal-autoatendimento-helpdesk

Portal de autoatendimento de helpdesk TI. MVP com três funções: abrir ticket (senha ou solicitação de software), listar tickets e consultar o status de um ticket. Backend em Flask + SQLite, templates HTML mínimos.

## Descrição / Description

**PT-BR.** Portal interno para usuários finais abrirem chamados de helpdesk sem ligar para o suporte. Suporta dois tipos de ticket: `senha` (redefinição de senha) e `software` (solicitação de instalação de software). Cada ticket fica com status `aberto` e pode ser consultado pelo ID.

**EN.** Internal portal for end users to open helpdesk tickets without calling support. Two ticket types: `senha` (password reset) and `software` (software installation request). Each ticket starts as `aberto` (open) and can be looked up by ID.

## Como usar / How to use

```bash
# 1. Entre na pasta do projeto
cd portal-autoatendimento-helpdesk

# 2. Instale as dependências
pip install -e .

# 3. Rode o servidor de desenvolvimento
flask run
```

Defina `FLASK_APP` se o comando `flask` não encontrar a aplicação automaticamente:

```bash
set FLASK_APP=portal_autoatendimento_helpdesk   # PowerShell/cmd
flask run
```

Abra `http://127.0.0.1:5000/` no navegador.

Rotas:

| Método | Caminho | O que faz |
|--------|---------|-----------|
| GET | `/` | Página inicial com lista de tickets recentes |
| GET | `/tickets` | Lista todos os tickets |
| GET/POST | `/tickets/novo` | Formulário para abrir um ticket (senha ou software) |
| GET | `/tickets/<id>` | Consulta o status de um ticket |

## Testes / Tests

A suíte usa `pytest` com o cliente de teste do Flask e um banco SQLite temporário por teste.

```bash
python -m pytest -q
```

Resultado esperado: 5 passed, incluindo criação e consulta de ticket.

## Licença / License

MIT License.

## Autor / Author

Kelvin Oliveira
