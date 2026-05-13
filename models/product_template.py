# © 2025 Aftermoves
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProductTemplate(models.Model):
    """
    Aplica token search a plantillas de producto.
    Busca en: name, default_code (referencia interna)
    """
    
    _name = "product.template"
    _inherit = ["product.template", "token.search.mixin"]
    
    # Campos donde buscar tokens
    _token_search_fields = ["name", "default_code", "barcode"]
    
    # Configuración específica para productos
    _token_min_length = 1  # Acepta tokens desde 1 char (incluye números como "70")
    _token_max_count = 8  # Máximo 8 tokens por búsqueda
    _token_min_count = 1  # Se activa con 1 token (útil para búsqueda parcial de barcode)
