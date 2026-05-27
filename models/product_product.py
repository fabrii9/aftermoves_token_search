# © 2025 Aftermoves
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ProductProduct(models.Model):
    """
    Aplica token search a variantes de producto.
    Busca en: name, default_code (referencia interna), barcode
    """

    _name = "product.product"
    _inherit = ["product.product", "token.search.mixin"]

    # Campos donde buscar tokens
    _token_search_fields = ["name", "default_code", "barcode"]

    # Configuración específica para productos
    _token_min_length = 1  # Acepta tokens desde 1 char (incluye números como "70")
    _token_max_count = 8  # Máximo 8 tokens por búsqueda
    _token_min_count = 1  # Se activa con 1 token (útil para búsqueda parcial de barcode)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        Override explícito para garantizar que el token search se aplique.
        El name_search estándar de product.product NO llama a super(),
        por lo que el mixin no se ejecuta por el MRO normal.
        """
        # Llamar al name_search estándar de Odoo (product_product.py)
        original_results = super(ProductProduct, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        # Aplicar búsqueda por tokens
        return self._apply_token_search(name, args, operator, limit, original_results)
