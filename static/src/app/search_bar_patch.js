/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

/**
 * Parche para ProductScreen que implementa búsqueda por tokens.
 * Replica el comportamiento del módulo aftermoves_token_search:
 * - Normaliza texto (lowercase, sin acentos)
 * - Separa en tokens (palabras individuales)
 * - Búsqueda AND (todos los tokens deben coincidir)
 * - Sin importar el orden de las palabras
 */

/**
 * Normaliza texto removiendo acentos y convirtiendo a minúsculas.
 * Igual que en Python: unicodedata.normalize('NFD') + remover diacríticos
 * 
 * @param {string} text - Texto a normalizar
 * @returns {string} Texto normalizado
 */
function normalizeText(text) {
    if (!text) return '';
    return text
        .toString()
        .toLowerCase()
        .normalize('NFD')  // Descompone caracteres con acentos
        .replace(/[\u0300-\u036f]/g, '');  // Remueve marcas diacríticas
}

/**
 * Tokeniza texto en palabras individuales, normalizando y filtrando.
 * 
 * @param {string} text - Texto a tokenizar
 * @param {number} minLength - Longitud mínima de tokens (default: 2)
 * @returns {Array<string>} Array de tokens normalizados
 */
function tokenizeSearch(text, minLength = 2) {
    if (!text) return [];
    
    const normalized = normalizeText(text);
    // Separar por espacios/puntuación y filtrar tokens cortos
    return normalized
        .split(/[\s\.,;:\-_\/\\]+/)
        .filter(token => token.length >= minLength);
}

/**
 * Parche del método getProductsBySearchWord de ProductScreen
 */
patch(ProductScreen.prototype, {
    /**
     * Sobrescribe la búsqueda de productos para usar tokens separados.
     * 
     * Comportamiento:
     * - "70lts negro" → busca productos que contengan "70lts" Y "negro"
     * - "negro 70" → mismo resultado (orden no importa)
     * - "cesto patron" → encuentra "CESTO PATRÓN" (sin acentos)
     * 
     * @param {string} searchWord - Texto de búsqueda del usuario
     * @returns {Array} Productos filtrados y ordenados
     */
    getProductsBySearchWord(searchWord) {
        // Tokenizar la búsqueda (min 2 caracteres por token)
        const tokens = tokenizeSearch(searchWord, 2);
        
        // Si no hay tokens válidos, retornar vacío
        if (tokens.length === 0) {
            return [];
        }
        
        // Obtener lista de productos a filtrar
        const products = this.pos.selectedCategory?.id
            ? this.getProductsByCategory(this.pos.selectedCategory)
            : this.products;
        
        // Filtrar productos que contengan TODOS los tokens
        const matches = products.filter((product) => {
            const productSearchString = normalizeText(product.searchString);
            
            // Verificar que el producto contenga todos los tokens (AND)
            return tokens.every(token => productSearchString.includes(token));
        });
        
        // Ordenar por relevancia:
        // 1. Productos donde el primer token aparece más temprano
        // 2. Ordenamiento alfabético como criterio de desempate
        return matches.sort((a, b) => {
            const nameA = normalizeText(a.searchString);
            const nameB = normalizeText(b.searchString);
            
            // Índice del primer token en cada producto
            const indexA = nameA.indexOf(tokens[0]);
            const indexB = nameB.indexOf(tokens[0]);
            
            // Ordenar por índice, luego alfabéticamente
            return indexA - indexB || nameA.localeCompare(nameB);
        });
    }
});

console.log('✅ Aftermoves Token Search: POS patched - multi-token AND search active');
