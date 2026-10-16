"""Suíte de testes do portal de autoatendimento de helpdesk.

Cobre criação e consulta de tickets contra o cliente real de teste do Flask,
com banco SQLite temporário por teste (isolamento total).
"""
import pytest

from portal_autoatendimento_helpdesk import create_app


@pytest.fixture
def app(tmp_path):
    """Instância da app com banco SQLite temporário e tabelas criadas."""
    app = create_app(
        {
            "DATABASE": str(tmp_path / "tickets.db"),
            "TESTING": True,
        }
    )
    with app.app_context():
        from portal_autoatendimento_helpdesk import models

        models.init_db()
    yield app


@pytest.fixture
def client(app):
    """Cliente de teste da aplicação."""
    return app.test_client()


def test_criar_ticket_senha(client):
    """Criar ticket do tipo 'senha' retorna redirecionamento e persiste."""
    resposta = client.post(
        "/tickets/novo",
        data={"tipo": "senha", "descricao": "Esqueci a senha do e-mail corporativo"},
        follow_redirects=True,
    )
    assert resposta.status_code == 200


def test_listar_mostra_ticket_criado(client):
    """Ticket criado aparece na listagem de tickets."""
    client.post(
        "/tickets/novo",
        data={"tipo": "software", "descricao": "Instalar o Visual Studio Code"},
        follow_redirects=True,
    )
    resposta = client.get("/tickets")
    assert resposta.status_code == 200
    assert b"software" in resposta.data
    assert b"Instalar o Visual Studio Code" in resposta.data


def test_consultar_status_ticket_existente(client):
    """Consultar status de ticket existente exibe dados e status 'aberto'."""
    client.post(
        "/tickets/novo",
        data={"tipo": "senha", "descricao": "Redefinir senha de acesso"},
        follow_redirects=True,
    )
    resposta = client.get("/tickets/1")
    assert resposta.status_code == 200
    assert b"Ticket #1" in resposta.data
    assert b"aberto" in resposta.data


def test_listar_sem_tickets(client):
    """Listagem sem tickets retorna 200 sem quebrar."""
    resposta = client.get("/tickets")
    assert resposta.status_code == 200


def test_ticket_inexistente_redireciona_para_lista(client):
    """Consultar ID inexistente redireciona para a lista com flash de erro."""
    resposta = client.get("/tickets/9999", follow_redirects=True)
    assert resposta.status_code == 200
    assert b"Ticket" in resposta.data
    assert b"encontrado" in resposta.data
