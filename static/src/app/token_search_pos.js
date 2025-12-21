/** @odoo-module */

import { ProductsWidget } from "@point_of_sale/app/screens/product_screen/product_list/product_list";
import { patch } from "@web/core/utils/patch";

/**
 * Extiende la búsqueda de productos en el POS para usar token_search
 */
patch(ProductsWidget.prototype, {
    /**
     * Normaliza texto para búsqueda (quita acentos, convierte a minúsculas)
     */
    _normalizeText(text) {
        if (!text) return "";
        return text
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
    },

    /**
     * Tokeniza el input de búsqueda
     */
    _tokenizeSearch(searchText) {
        if (!searchText) return [];
        
        const normalized = this._normalizeText(searchText);
        // Separar por espacios, comas, puntos, etc
        const tokens = normalized
            .split(/[\s,\.\-_\/]+/)
            .filter(token => token.length > 0);
        
        return tokens;
    },

    /**
     * Override del método de búsqueda para incluir token search
     */
    get productsToDisplay() {
        let products = super.productsToDisplay;
        
        // Si hay texto de búsqueda, aplicar token search
        const searchWord = this.searchWord;
        if (searchWord && searchWord.length > 0) {
            const tokens = this._tokenizeSearch(searchWord);
            
            if (tokens.length > 0) {
                // Filtrar productos que contengan TODOS los tokens
                products = products.filter(product => {
                    // Construir texto de búsqueda del producto
                    const productText = this._normalizeText(
                        [
                            product.display_name || "",
                            product.default_code || "",
                            product.barcode || ""
                        ].join(" ")
                    );
                    
                    // Verificar que TODOS los tokens estén presentes
                    return tokens.every(token => productText.includes(token));
                });
            }
        }
        
        return products;
    }
});

console.log("✅ Aftermoves Token Search: POS search extension loaded");
