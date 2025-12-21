# © 2025 Aftermoves
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrModel(models.Model):
    """
    Extiende ir.model para agregar flag de token search por modelo.
    Compatible con base_name_search_improved.
    """
    
    _inherit = "ir.model"
    
    token_search_enabled = fields.Boolean(
        string="Token Search Enabled",
        default=False,
        help="Enable advanced token-based search for this model. "
             "This allows finding records by loose word matching, "
             "even when words are not adjacent. "
             "Example: 'CESTO RECT 70LTS' finds 'CESTO SAN REMO RECT. SLIM C/TAPA X 70LTS'"
    )
