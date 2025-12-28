/** @odoo-module **/

import { SearchModel } from "@web/search/search_model";
import { patch } from "@web/core/utils/patch";

console.log('[AFTERMOVES_V7] Token Search Widget cargado');

/**
 * Patch del SearchModel para búsqueda incremental con AND
 * Estrategia: Acumular tokens y pasarlos todos juntos separados por espacios
 * El backend (_search_token_search) se encargará de dividirlos y aplicar AND
 */

// Estado global para tokens acumulados por searchItemId
const intelligentSearchState = {};

patch(SearchModel.prototype, {
    /**
     * Intercepta addAutoCompletionValues para acumular búsquedas en token_search
     */
    addAutoCompletionValues(searchItemId, autocompleteValue) {
        const searchItem = this.searchItems[searchItemId];
        
        console.log('[AFTERMOVES_V7] addAutoCompletionValues:', searchItem?.fieldName, autocompleteValue.value);
        
        // Detectar si es una búsqueda en token_search
        if (searchItem && searchItem.fieldName === 'token_search') {
            console.log('[AFTERMOVES_V7] Búsqueda en token_search detectada');
            
            // Verificar si hay algún filtro activo de token_search en el query actual
            const hasActiveTokenSearch = this.query.some(queryElem => {
                const item = this.searchItems[queryElem.searchItemId];
                return item && item.fieldName === 'token_search';
            });
            
            // Si no hay filtro activo, significa que fue borrado - limpiar el estado
            if (!hasActiveTokenSearch && intelligentSearchState[searchItemId]) {
                console.log('[AFTERMOVES_V7] No hay filtro activo, limpiando estado para empezar de cero');
                delete intelligentSearchState[searchItemId];
            }
            
            // Inicializar el estado si no existe
            if (!intelligentSearchState[searchItemId]) {
                intelligentSearchState[searchItemId] = {
                    tokens: []
                };
            }
            
            // Agregar el nuevo token
            const newToken = autocompleteValue.value.trim();
            if (newToken && !intelligentSearchState[searchItemId].tokens.includes(newToken)) {
                intelligentSearchState[searchItemId].tokens.push(newToken);
            }
            
            console.log('[AFTERMOVES_V7] Tokens acumulados:', intelligentSearchState[searchItemId].tokens);
            
            // Remover búsquedas anteriores de token_search del query
            this.query = this.query.filter(queryElem => {
                const item = this.searchItems[queryElem.searchItemId];
                return !(item && item.fieldName === 'token_search');
            });
            
            // Crear un valor único que contenga todos los tokens separados por espacios
            // El backend los dividirá y aplicará AND
            const combinedValue = intelligentSearchState[searchItemId].tokens.join(' ');
            
            console.log('[AFTERMOVES_V7] Valor combinado a buscar:', combinedValue);
            
            // Modificar el autocompleteValue con todos los tokens
            // IMPORTANTE: El label es lo que se usa en el domain, debe ser el valor limpio
            const modifiedAutocompleteValue = {
                ...autocompleteValue,
                value: combinedValue,
                label: combinedValue,  // Sin decoración - Odoo usa esto en el domain
            };
            
            // Llamar al método original
            super.addAutoCompletionValues(searchItemId, modifiedAutocompleteValue);
            
            return;
        }
        
        // Para otros campos, comportamiento normal
        super.addAutoCompletionValues(searchItemId, autocompleteValue);
    },
});

