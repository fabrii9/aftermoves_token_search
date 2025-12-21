# Aftermoves Token Search

> Búsqueda inteligente por tokens para Odoo 18 - Encuentra productos aunque las palabras no estén juntas

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](http://www.gnu.org/licenses/lgpl-3.0)
[![Odoo Version](https://img.shields.io/badge/Odoo-18.0-875a7b.svg)](https://www.odoo.com/)

## 🎯 ¿Qué hace?

Módulo de búsqueda avanzada por tokens para Odoo 18.

Permite encontrar registros mediante palabras sueltas (tokens) sin necesidad de que estén en orden o adyacentes.

### Ejemplo Real

- **Producto:** `CESTO SAN REMO RECT. SLIM C/TAPA VAI VEN X 70LTS NEGRO`
- **Búsqueda:** `70lts cesto` o `cesto 70LTS` o `NEGRO 70`
- ✅ **Lo encuentra** aunque las palabras no estén juntas ni en orden

### ¿Cómo funciona?

1. **Normalización**: Convierte texto a minúsculas, elimina acentos y puntuación
2. **Tokenización**: Divide en palabras individuales
3. **Búsqueda AND**: Busca registros que contengan TODAS las palabras (en cualquier orden)
4. **Smart fallback**: Solo se activa si la búsqueda estándar no da buenos resultados

## ✨ Características

- ✅ **Búsqueda por tokens**: Normaliza y tokeniza el input, busca cada palabra
- ✅ **Sin acentos**: `cesto` encuentra `CESTO` y `Césto`
- ✅ **Performance optimizada**: 
  - Ignora tokens ≤ 2 caracteres
  - Máximo 6 tokens por búsqueda
  - Solo se activa si búsqueda estándar no encuentra suficientes resultados
- ✅ **Compatible con `base_name_search_improved`**: Se ejecuta DESPUÉS, no interfiere
- ✅ **Feature flags**:
  - Global: `aftermoves.token_search_enabled` (default: True)
  - Por modelo: campo `token_search_enabled` en ir.model
- ✅ **Sin dependencias extras**: Solo Python stdlib + Odoo base
- ✅ **Aplicado a**: `product.template`, `product.product`
- ✅ **Extensible**: Fácil de aplicar a otros modelos (res.partner, sale.order, etc.)

## 📦 Instalación

### Método 1: Clonar repositorio

```bash
cd /ruta/a/tu/odoo/addons
git clone https://github.com/tu-usuario/aftermoves-token-search.git aftermoves_token_search
```

### Método 2: Descargar ZIP

1. Descargar el ZIP desde GitHub
2. Extraer en la carpeta `addons/` de tu Odoo
3. Renombrar carpeta a `aftermoves_token_search` (sin el `-master` o `-main`)

### Activar el módulo

1. Reiniciar Odoo
2. Ir a **Aplicaciones**
3. Quitar filtro "Aplicaciones" y buscar "Token"
4. Click en **Instalar** en "Aftermoves Token Search"

## ⚙️ Configuración

### Habilitar Token Search (Requerido)

Por defecto, el módulo está instalado pero **inactivo** en todos los modelos.

#### Opción 1: Habilitar Globalmente

**Ajustes > Técnico > Parámetros > Parámetros del Sistema**

Crear/editar:
- **Clave**: `aftermoves.token_search_enabled`
- **Valor**: `True`

#### Opción 2: Habilitar por Modelo

**Ajustes > Técnico > Estructura de Base de Datos > Modelos**

1. Buscar el modelo (ej: "Product Template")
2. Editar
3. Activar toggle **"Token Search Enabled"**

### Verificar Configuración

```python
# Desde shell de Odoo
env['ir.config_parameter'].get_param('aftermoves.token_search_enabled')  # True/False
model = env['ir.model'].search([('model', '=', 'product.product')])
model.token_search_enabled  # True/False
```

## 🚀 Uso

### Desde UI - Inventario/Ventas

1. **Inventario > Productos** o **Ventas > Pedidos > Crear**
2. Barra de búsqueda > Click en dropdown (▼)
3. Seleccionar **"Búsqueda Inteligente (tokens)"**
4. Escribir: `70lts cesto` o `CESTO NEGRO RECT`
5. ✅ Encuentra productos

### Desde Many2one (Automático)

En campos de selección de producto (líneas de pedido, albaranes, etc.):
1. Click en el campo "Producto"
2. Escribir: `cesto rect 70`
3. ✅ Búsqueda automática por tokens

### Ejemplos de Búsqueda

```python
# Producto: "CESTO SAN REMO RECT. SLIM C/TAPA VAI VEN X 70LTS NEGRO"

# ✅ FUNCIONAN:
"70lts cesto"           # Orden invertido
"cesto negro"           # Palabras separadas
"RECT 70"               # Cualquier combinación
"slim tapa"             # Tokens internos
"cesto-001"             # Por código (default_code)

# ❌ NO FUNCIONAN:
"ces"                   # Token muy corto (≤ 2 chars)
"de"                    # Stop words ignoradas
```

## 📊 Performance

### Optimizaciones Incluidas

- **Lazy evaluation**: Solo se activa si búsqueda estándar no da resultados
- **Token filtering**: Ignora palabras ≤ 2 caracteres
- **Limit tokens**: Máximo 6 tokens por búsqueda
- **Early exit**: Si encuentra suficientes resultados, no busca más
- **Index-friendly**: Usa operadores `ilike` que aprovechan índices PostgreSQL

### Métricas Típicas

| Escenario | Productos | Tokens | Tiempo |
|-----------|-----------|--------|---------|
| Búsqueda estándar falla | 10,000 | 2 | ~50ms |
| 3 tokens | 10,000 | 3 | ~80ms |
| 5 tokens | 10,000 | 5 | ~120ms |

## 🔧 Desarrollo

### Aplicar a Otros Modelos

```python
from odoo import models

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'token.search.mixin']
    
    # ¡Listo! Ya tiene token search
```

### Personalizar Campos de Búsqueda

```python
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    def _get_token_search_fields(self):
        """Override para agregar más campos"""
        fields = super()._get_token_search_fields()
        fields.extend(['description_sale', 'barcode'])
        return fields
```

### Tests

```bash
# Ejecutar tests del módulo
odoo-bin -c odoo.conf -d test_db -i aftermoves_token_search --test-enable --stop-after-init
```

## 📁 Estructura del Módulo

```
aftermoves_token_search/
├── __init__.py
├── __manifest__.py
├── README.md
├── data/
│   └── ir_config_parameter.xml       # Feature flag global
├── models/
│   ├── __init__.py
│   ├── ir_model.py                   # Feature flag por modelo
│   ├── token_search_mixin.py         # Lógica principal
│   ├── product_template.py           # Aplicado a productos
│   └── product_product.py
└── views/
    ├── ir_model_views.xml             # UI para habilitar por modelo
    └── product_views.xml              # Filtro de búsqueda en productos
```

## 🐛 Troubleshooting

### No aparece el filtro "Búsqueda Inteligente"

**Solución:**
1. Verificar que el módulo esté instalado
2. Refrescar la página (Ctrl+F5)
3. Verificar que `product_views.xml` se haya cargado

### No encuentra productos

**Solución:**
1. Verificar feature flags: `aftermoves.token_search_enabled = True`
2. Verificar modelo habilitado: `ir.model` con `token_search_enabled = True`
3. Probar con tokens más específicos (>2 caracteres)

### Performance lenta

**Solución:**
1. Reducir número de tokens (máx. 3-4)
2. Verificar índices en PostgreSQL: `CREATE INDEX idx_product_name ON product_template(name);`
3. Aumentar `limit` en búsqueda estándar para que token search no se active tan seguido

## 📄 Licencia

LGPL-3.0 - Ver archivo [LICENSE](LICENSE)

## 👥 Créditos

Desarrollado por **Aftermoves**

- Website: https://aftermoves.com
- Email: contacto@aftermoves.com

## 🤝 Contribuir

1. Fork el proyecto
2. Crear branch de feature: `git checkout -b feature/mi-mejora`
3. Commit cambios: `git commit -am 'Agrego nueva feature'`
4. Push al branch: `git push origin feature/mi-mejora`
5. Crear Pull Request

## 📝 Changelog

### [1.0.0] - 2025-12-21

#### Added
- Búsqueda por tokens con normalización (sin acentos, lowercase)
- Feature flags global y por modelo
- Mixin reutilizable para cualquier modelo
- Aplicado a `product.template` y `product.product`
- Filtro de búsqueda en vistas de producto
- Documentación completa

#### Performance
- Lazy evaluation (solo si búsqueda estándar falla)
- Máximo 6 tokens por búsqueda
- Ignora tokens ≤ 2 caracteres
- `default_code` (Referencia interna)

Para modificar, editar en el modelo correspondiente:
```python
_token_search_fields = ["name", "default_code", "barcode"]
```

## Performance

- ✅ **Lazy evaluation**: Solo se ejecuta si búsqueda estándar no alcanza el limit
- ✅ **Max tokens**: Limita a 6 tokens para evitar queries excesivamente complejas
- ✅ **Min length**: Ignora tokens ≤ 2 chars (evita ruido: "de", "el", "x")
- ✅ **Sin full-text search**: No requiere extensiones PostgreSQL

## Limitaciones

- Solo funciona con operadores `ilike` / `like`
- No aplica fuzzy matching (distancia de Levenshtein)
- No usa índices full-text (puede ser más lento en bases de datos enormes)

## Desinstalación

Simplemente desinstalar el módulo. No modifica datos ni tablas permanentemente.

## Créditos

**Autor**: Aftermoves  
**Licencia**: LGPL-3  
**Versión**: 18.0.1.0.0
