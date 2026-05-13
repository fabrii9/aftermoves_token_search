# © 2025 Aftermoves
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class SaleOrder(models.Model):
    """
    Aplica token search a presupuestos de venta.
    Busca en: name, client_order_ref, origin
    """

    _name = "sale.order"
    _inherit = ["sale.order", "token.search.mixin"]

    # Campos donde buscar tokens
    _token_search_fields = ["name", "client_order_ref", "origin"]

    # Configuración específica para ventas
    _token_min_length = 1  # Acepta tokens desde 1 char
    _token_max_count = 8  # Máximo 8 tokens por búsqueda
