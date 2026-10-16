"""Rotas HTTP do portal de helpdesk.

Endpoints
---------
- ``GET /`` : página inicial com lista de tickets e link para abrir novo.
- ``GET /tickets`` : lista todos os tickets.
- ``GET/POST /tickets/novo`` : formulário para abrir um ticket.
- ``GET /tickets/<int:ticket_id>`` : consulta o status de um ticket.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import models

bp = Blueprint("helpdesk", __name__)


@bp.route("/")
def index():
    """Página inicial: lista tickets recentes e expõe o link de novo ticket."""
    tickets = models.listar_tickets()
    return render_template("index.html", tickets=tickets)


@bp.route("/tickets", methods=["GET"])
def listar_tickets_route():
    """Lista todos os tickets cadastrados."""
    tickets = models.listar_tickets()
    return render_template("tickets.html", tickets=tickets)


@bp.route("/tickets/novo", methods=["GET", "POST"])
def novo_ticket():
    """Abre um novo ticket (senha ou solicitação de software)."""
    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        if tipo not in models.TIPOS_VALIDOS:
            flash("Tipo inválido. Use 'senha' ou 'solicitação de software'.", "erro")
            return render_template("novo_ticket.html"), 400
        if not descricao:
            flash("A descrição é obrigatória.", "erro")
            return render_template("novo_ticket.html"), 400
        models.criar_ticket(tipo, descricao)
        flash("Ticket aberto com sucesso.", "sucesso")
        return redirect(url_for("helpdesk.listar_tickets_route"))
    return render_template("novo_ticket.html")


@bp.route("/tickets/<int:ticket_id>")
def ticket_detalhe(ticket_id: int):
    """Consulta o status e dados de um ticket existente."""
    ticket = models.obter_ticket(ticket_id)
    if ticket is None:
        flash("Ticket não encontrado.", "erro")
        return redirect(url_for("helpdesk.listar_tickets_route"))
    return render_template("ticket_detail.html", ticket=ticket)
