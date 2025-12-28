# © 2025 Aftermoves
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Aftermoves Token Search",
    "summary": "Advanced token-based search for products and other models",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "website": "https://aftermoves.com",
    "author": "Aftermoves",
    "license": "LGPL-3",
    "depends": [
        "base",
        "product",  # Para aplicar a productos
        "web",      # Para los assets JavaScript
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "views/ir_model_views.xml",
        "views/product_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "aftermoves_token_search/static/src/js/intelligent_search_widget.js",
            "aftermoves_token_search/static/src/css/intelligent_search.css",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
