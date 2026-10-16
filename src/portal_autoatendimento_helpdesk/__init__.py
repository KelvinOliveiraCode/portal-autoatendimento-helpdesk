"""Aplicação Flask do portal de autoatendimento de helpdesk TI.

Expõe a fábrica ``create_app`` usada tanto em produção quanto nos testes.
"""
import os
from flask import Flask

from .routes import bp


def create_app(test_config=None):
    """Cria e configura a instância da aplicação Flask.

    Parâmetros
    ----------
    test_config : dict, opcional
        Sobrescreve as configurações padrão quando informado (usado nos testes
        para aponta o banco para um arquivo temporário).
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "tickets.db"),
        SECRET_KEY="dev",
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        # A pasta de instância já existe; não há o que fazer.
        pass

    from . import models

    models.init_app(app)
    app.register_blueprint(bp)

    return app
