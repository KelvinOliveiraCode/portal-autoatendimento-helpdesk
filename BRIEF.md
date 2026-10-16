# BRIEF — portal-autoatendimento-helpdesk

**Projeto:** portal-autoatendimento-helpdesk  
**Área:** Suporte TI  
**Stack:** Python + Flask + SQLite  
**Local:** `C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\portal-autoatendimento-helpdesk\`

## Entregas

| Arquivo | O que é |
|---------|---------|
| `pyproject.toml` | Declaração do projeto e dependência (`Flask>=3.0,<4.0`) |
| `src/portal_autoatendimento_helpdesk/__init__.py` | Fábrica `create_app` com `SECRET_KEY` e `DATABASE` configuráveis |
| `src/portal_autoatendimento_helpdesk/models.py` | Camada SQLite: `Ticket` (dataclass), `criar_ticket`, `listar_tickets`, `obter_ticket` |
| `src/portal_autoatendimento_helpdesk/routes.py` | Rotas: `GET /`, `GET /tickets`, `GET/POST /tickets/novo`, `GET /tickets/<id>` |
| `src/portal_autoatendimento_helpdesk/templates/*.html` | Templates Jinja2 mínimos (base, índice, lista, novo ticket, detalhe) |
| `tests/test_tickets.py` | Suíte pytest: 5 testes (criação, listagem, consulta de status, lista vazia, ID inexistente) |
| `README.md` | Bilíngue PT-BR + EN: título, descrição, como usar com `flask run`, testes, licença MIT, autor |
| `BRIEF.md` | Este documento |

## Critérios de aceitação (MVP)

- [x] Portal funcional (abrir ticket senha/software, listar, consultar status)
- [x] Testes que passem (`python -m pytest -q`)
- [x] README PT/EN completo

## Como verificar

```bash
cd C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\portal-autoatendimento-helpdesk
pip install -e .
python -m pytest -q
# esperado: 5 passed

# opcional: rodar o servidor
flask run   # (defina FLASK_APP=portal_autoatendimento_helpdesk se necessário)
# então abra http://127.0.0.1:5000/
```

## Validação

Responsável: workflow manager (o solicitante). Confirme os testes acima e liberte o entregável.
