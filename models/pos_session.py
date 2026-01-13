# © 2025 Aftermoves
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _pos_ui_models_to_load(self):
        """Asegurar que product.product está en la lista de modelos a cargar"""
        result = super()._pos_ui_models_to_load()
        if 'product.product' not in result:
            result.append('product.product')
        return result

    def _loader_params_product_product(self):
        """Agregar campos necesarios para la búsqueda por tokens"""
        result = super()._loader_params_product_product()
        # Asegurar que los campos de búsqueda estén disponibles
        search_fields = result.get('search_params', {}).get('fields', [])
        
        # Agregar campos si no están
        for field in ['default_code', 'barcode']:
            if field not in search_fields:
                search_fields.append(field)
        
        return result
