# © 2025 Aftermoves
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
import re
import unicodedata

from odoo import api, fields, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class TokenSearchMixin(models.AbstractModel):
    """
    Mixin que proporciona búsqueda avanzada por tokens.
    
    Características:
    - Normaliza el input (lowercase, sin acentos, puntuación como espacios)
    - Tokeniza en palabras/números
    - Busca cada token con ILIKE (AND)
    - Ignora tokens muy cortos (≤ 2 chars)
    - Limita cantidad de tokens (max 6)
    - Solo se activa si la búsqueda estándar no devuelve suficientes resultados
    """
    
    _name = "token.search.mixin"
    _description = "Token Search Mixin"
    
    # Campo virtual para búsquedas en vistas de lista/kanban
    token_search = fields.Char(
        string="Token Search",
        compute="_compute_token_search",
        search="_search_token_search",
        store=False,
    )
    
    # Configuración por defecto (puede sobreescribirse en modelos herederos)
    _token_search_fields = None  # Lista de campos donde buscar. Si None, usa _rec_names
    _token_min_length = 2  # Tokens más cortos se ignoran
    _token_max_count = 6  # Máximo de tokens a procesar
    
    def _compute_token_search(self):
        """Campo virtual, no tiene valor real"""
        for record in self:
            record.token_search = False
    
    @api.model
    def _search_token_search(self, operator, value):
        """
        Método de búsqueda para el campo virtual token_search.
        Permite usar este campo en vistas de búsqueda (<search>).
        
        :param operator: Operador (ilike, like, =, etc.)
        :param value: Valor a buscar
        :return: Dominio Odoo
        """
        if not value or operator not in ('ilike', 'like', '='):
            return [('id', '=', False)]
        
        # Tokenizar
        tokens = self._tokenize_search_input(
            value,
            min_length=self._token_min_length,
            max_count=self._token_max_count
        )
        
        if not tokens:
            return [('id', '=', False)]
        
        # Construir dominio
        domain = self._build_token_search_domain(tokens)
        
        return domain if domain else [('id', '=', False)]
    
    @classmethod
    def _normalize_search_text(cls, text):
        """
        Normaliza texto para búsqueda:
        - Convierte a minúsculas
        - Remueve acentos
        - Reemplaza puntuación por espacios
        - Normaliza espacios múltiples
        
        :param text: Texto a normalizar
        :return: Texto normalizado
        """
        if not text:
            return ""
        
        # Lowercase
        text = text.lower()
        
        # Remover acentos usando unicodedata
        # NFD = Canonical Decomposition
        # Filtra caracteres de categoría Mn (Nonspacing_Mark)
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        
        # Reemplazar puntuación y caracteres especiales por espacios
        # Mantiene solo letras, números y espacios
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Normalizar espacios múltiples a uno solo
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @classmethod
    def _tokenize_search_input(cls, text, min_length=2, max_count=6):
        """
        Tokeniza el input de búsqueda.
        
        :param text: Texto a tokenizar
        :param min_length: Longitud mínima del token
        :param max_count: Cantidad máxima de tokens
        :return: Lista de tokens únicos
        """
        if not text:
            return []
        
        # Normalizar
        normalized = cls._normalize_search_text(text)
        
        # Separar por espacios
        tokens = normalized.split()
        
        # Filtrar por longitud mínima
        tokens = [t for t in tokens if len(t) > min_length]
        
        # Eliminar duplicados manteniendo orden
        seen = set()
        unique_tokens = []
        for token in tokens:
            if token not in seen:
                seen.add(token)
                unique_tokens.append(token)
        
        # Limitar cantidad
        return unique_tokens[:max_count]
    
    def _get_token_search_fields(self):
        """
        Obtiene los campos donde buscar tokens.
        Por defecto usa _rec_name, pero puede sobreescribirse.
        
        :return: Lista de nombres de campos
        """
        if self._token_search_fields:
            return self._token_search_fields
        
        # Por defecto busca en el campo rec_name
        return [self._rec_name] if self._rec_name else ['name']
    
    def _is_token_search_enabled(self):
        """
        Verifica si la búsqueda por tokens está habilitada.
        
        Chequea:
        1. Parámetro global aftermoves.token_search_enabled
        2. Flag por modelo (si existe, ej: desde base_name_search_improved)
        
        :return: Boolean
        """
        # Feature flag global
        global_enabled = self.env['ir.config_parameter'].sudo().get_param(
            'aftermoves.token_search_enabled',
            default='True'
        )
        
        if global_enabled.lower() not in ('true', '1', 'yes'):
            return False
        
        # Feature flag por modelo (compatible con base_name_search_improved)
        try:
            model = self.env['ir.model'].sudo().search([
                ('model', '=', self._name)
            ], limit=1)
            
            if model and hasattr(model, 'token_search_enabled'):
                return model.token_search_enabled
        except Exception as e:
            _logger.debug(
                "Could not check model-level token_search_enabled: %s", e
            )
        
        # Por defecto, habilitado si el flag global está en True
        return True
    
    def _build_token_search_domain(self, tokens, base_domain=None):
        """
        Construye el dominio de búsqueda por tokens.
        
        Cada token debe estar presente en al menos uno de los campos (OR),
        pero TODOS los tokens deben matchear (AND).
        
        Ejemplo:
        tokens = ['cesto', 'rect', '70lts']
        fields = ['name', 'default_code']
        
        Resultado:
        [
            '&', '&',
            '|', ('name', 'ilike', 'cesto'), ('default_code', 'ilike', 'cesto'),
            '|', ('name', 'ilike', 'rect'), ('default_code', 'ilike', 'rect'),
            '|', ('name', 'ilike', '70lts'), ('default_code', 'ilike', '70lts'),
        ]
        
        :param tokens: Lista de tokens a buscar
        :param base_domain: Dominio base a combinar con AND
        :return: Dominio Odoo
        """
        if not tokens:
            return base_domain or []
        
        search_fields = self._get_token_search_fields()
        
        if not search_fields:
            return base_domain or []
        
        # Construir dominio para cada token
        token_domains = []
        for token in tokens:
            # OR: el token debe estar en al menos un campo
            field_conditions = [
                (field, 'ilike', token) for field in search_fields
            ]
            token_domain = expression.OR([
                [condition] for condition in field_conditions
            ])
            token_domains.append(token_domain)
        
        # AND: todos los tokens deben matchear
        final_domain = token_domains[0] if token_domains else []
        for token_domain in token_domains[1:]:
            final_domain = expression.AND([final_domain, token_domain])
        
        # Combinar con dominio base
        if base_domain:
            final_domain = expression.AND([base_domain, final_domain])
        
        return final_domain
    
    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """
        Override de name_search que agrega búsqueda por tokens.
        
        Comportamiento:
        1. Ejecuta búsqueda estándar (super) primero
        2. Si hay suficientes resultados, retorna directamente
        3. Si no, intenta búsqueda por tokens
        4. Combina resultados sin duplicados
        
        :param name: Texto de búsqueda
        :param args: Dominio adicional
        :param operator: Operador de búsqueda (solo funciona con 'ilike' o 'like')
        :param limit: Límite de resultados
        :return: Lista de tuplas (id, display_name)
        """
        # Ejecutar búsqueda estándar primero (respeta base_name_search_improved)
        original_results = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        
        # Si no hay nombre o ya tenemos suficientes resultados, retornar
        if not name or (limit and len(original_results) >= limit):
            return original_results
        
        # Solo aplicar con operadores ilike/like
        if operator not in ('ilike', 'like'):
            return original_results
        
        # Verificar si está habilitado
        if not self._is_token_search_enabled():
            return original_results
        
        try:
            # Tokenizar input
            tokens = self._tokenize_search_input(
                name,
                min_length=self._token_min_length,
                max_count=self._token_max_count
            )
            
            # Si no hay tokens válidos o solo hay 1, no aplicar
            # (la búsqueda estándar ya lo hizo)
            if len(tokens) < 2:
                return original_results
            
            _logger.debug(
                "Token search on %s: input='%s' -> tokens=%s",
                self._name, name, tokens
            )
            
            # IDs ya encontrados (para evitar duplicados)
            seen_ids = {res[0] for res in original_results}
            
            # Calcular cuántos resultados más necesitamos
            remaining_limit = None
            if limit:
                remaining_limit = limit - len(original_results)
                if remaining_limit <= 0:
                    return original_results
            
            # Construir dominio por tokens
            base_domain = args or []
            token_domain = self._build_token_search_domain(tokens, base_domain)
            
            # Agregar exclusión de IDs ya vistos
            if seen_ids:
                token_domain = expression.AND([
                    token_domain,
                    [('id', 'not in', list(seen_ids))]
                ])
            
            # Buscar
            additional_ids = self._search(
                token_domain,
                limit=remaining_limit
            )
            
            if additional_ids:
                # Convertir a records y obtener display_name
                additional_records = self.browse(additional_ids)
                additional_results = [
                    (rec.id, rec.display_name) for rec in additional_records
                ]
                
                _logger.debug(
                    "Token search found %d additional results",
                    len(additional_results)
                )
                
                # Combinar resultados
                return original_results + additional_results
            
        except Exception as e:
            # Si algo falla, loggear pero no romper la búsqueda
            _logger.warning(
                "Token search failed on %s with input '%s': %s",
                self._name, name, e
            )
        
        return original_results
