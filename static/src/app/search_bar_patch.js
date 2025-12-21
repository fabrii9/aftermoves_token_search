/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

/**
 * Extiende la búsqueda del POS para usar token_search normalizado (sin acentos).
 * Sobrescribe getProductsBySearchWord para normalizar tanto la búsqueda como
 * el searchString de los productos antes de comparar.
 */

/**
 * Normaliza texto removiendo acentos y convirtiendo a minúsculas
 * (igual que en Python: unicodedata.normalize('NFD') + remover diacríticos)
 */
function normalizeText(text) {
    if (!text) return '';
    return text
        .toString()
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '');
}

/**
 * Parche para PosStore.getProductsBySearchWord
 */
patch(PosStore.prototype, {
    /**
     * Sobrescribe getProductsBySearchWord para normalizar texto antes de buscar
     */
    getProductsBySearchWord(searchWord, products) {
        const words = normalizeText(searchWord);
        
        const matches = products.filter(
            (p) => {
                // Normalizar el searchString del producto antes de comparar
                const productSearchString = normalizeText(p.searchString);
                
                // Verificar si coincide
                if (productSearchString.includes(words)) {
                    return true;
                }
                
                // También buscar en variantes si existen
                if (p.product_variant_ids && p.product_variant_ids.length > 0) {
                    return p.product_variant_ids.some((variant) =>
                        normalizeText(variant.searchString).includes(words)
                    );
                }
                
                return false;
            }
        );

        // Usar el método original para ordenar
        return this.sortByWordIndex(matches, words);
    }
});

console.log('✅ Token Search: POS search patched - accent-insensitive search enabled');
