"""Camada de dados: tickets armazenados em SQLite.

A única dependência externa é a biblioteca padrão ``sqlite3``. Não há ORM.
"""
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from flask import g, current_app

TIPOS_VALIDOS = ("senha", "software")
STATUS_PADRAO = "aberto"


@dataclass(frozen=True)
class Ticket:
    """Registro imutável de um ticket de helpdesk."""

    id: Optional[int]
    tipo: str
    descricao: str
    status: str
    criado_em: str


def get_db():
    """Retorna a conexão SQLite aberta no contexto da requisição."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exception=None):
    """Fecha a conexão SQLite ao encerrar o contexto da aplicação."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria a tabela de tickets caso ainda não exista."""
    with closing(get_db()) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL CHECK (tipo IN ('senha', 'software')),
                descricao TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'aberto',
                criado_em TEXT NOT NULL
            )
            """
        )
        db.commit()


def init_app(app):
    """Registra o teardown da conexão e inicializa o banco no contexto."""
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()


def _now() -> str:
    """Retorna o horário atual em ISO 8601 (UTC)."""
    return datetime.now(timezone.utc).isoformat()


def criar_ticket(tipo: str, descricao: str) -> int:
    """Insere um novo ticket e retorna o seu ID gerado."""
    if tipo not in TIPOS_VALIDOS:
        raise ValueError(f"tipo inválido: {tipo!r}; use um de {TIPOS_VALIDOS}")
    if not descricao or not descricao.strip():
        raise ValueError("descricao é obrigatória")
    db = get_db()
    cur = db.execute(
        "INSERT INTO tickets (tipo, descricao, status, criado_em) VALUES (?, ?, ?, ?)",
        (tipo, descricao.strip(), STATUS_PADRAO, _now()),
    )
    db.commit()
    return cur.lastrowid


def listar_tickets():
    """Retorna todos os tickets ordenados do mais recente para o mais antigo."""
    db = get_db()
    rows = db.execute(
        "SELECT id, tipo, descricao, status, criado_em "
        "FROM tickets ORDER BY id DESC"
    ).fetchall()
    return [
        Ticket(
            id=row["id"],
            tipo=row["tipo"],
            descricao=row["descricao"],
            status=row["status"],
            criado_em=row["criado_em"],
        )
        for row in rows
    ]


def obter_ticket(ticket_id: int) -> Optional[Ticket]:
    """Retorna o ticket pelo ID, ou ``None`` quando não encontrado."""
    db = get_db()
    row = db.execute(
        "SELECT id, tipo, descricao, status, criado_em FROM tickets WHERE id = ?",
        (ticket_id,),
    ).fetchone()
    if row is None:
        return None
    return Ticket(
        id=row["id"],
        tipo=row["tipo"],
        descricao=row["descricao"],
        status=row["status"],
        criado_em=row["criado_em"],
    )
