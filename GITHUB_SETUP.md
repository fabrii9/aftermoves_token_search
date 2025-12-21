# 🚀 Instrucciones para Subir a GitHub

## Paso 1: Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `aftermoves-token-search`
3. Descripción: `Advanced token-based search for Odoo 18 - Find products even if words are not together`
4. **Visibilidad**: 
   - ✅ **Public** (si querés compartir)
   - ⬜ Private (si es solo para vos)
5. **NO marcar** "Initialize with README" (ya lo tenés)
6. Click **"Create repository"**

## Paso 2: Conectar Repositorio Local con GitHub

Después de crear el repo, GitHub te mostrará comandos. Usá estos:

```bash
cd /Users/fabrizio/Documents/code/odoov18-enterprise-mundolimpio/addons/aftermoves_token_search

# Agregar remote (reemplazá TU-USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU-USUARIO/aftermoves-token-search.git

# Subir cambios
git push -u origin main
```

## Paso 3: Verificar que Subió

Ve a tu repo en GitHub: `https://github.com/TU-USUARIO/aftermoves-token-search`

Deberías ver:
- ✅ README.md con toda la documentación
- ✅ Carpetas: `data/`, `models/`, `views/`
- ✅ Archivos: `__manifest__.py`, `__init__.py`

## Paso 4: Agregar Topics (Opcional)

En GitHub, en la página del repo:
1. Click en ⚙️ (engranaje) arriba a la derecha
2. En "Topics" agregá:
   - `odoo`
   - `odoo-18`
   - `odoo-module`
   - `search`
   - `product-search`
   - `token-search`
3. Save changes

## 🎯 Resultado Final

Tu repo quedará como:

```
https://github.com/TU-USUARIO/aftermoves-token-search
├── README.md              ← Documentación completa
├── .gitignore            ← Ignora __pycache__ y .pyc
├── __manifest__.py       ← Metadata del módulo
├── data/
│   └── ir_config_parameter.xml
├── models/
│   ├── token_search_mixin.py  ← Lógica principal
│   ├── product_template.py
│   └── ...
└── views/
    ├── product_views.xml
    └── ...
```

## 📦 Instalación desde GitHub (para otros usuarios)

Compartí estas instrucciones:

### Opción A: Clonar directamente

```bash
cd /ruta/a/odoo/addons
git clone https://github.com/TU-USUARIO/aftermoves-token-search.git aftermoves_token_search
```

### Opción B: Descargar ZIP

1. En GitHub, click en botón verde **"Code"**
2. **Download ZIP**
3. Extraer en `addons/`
4. Renombrar carpeta a `aftermoves_token_search`

Luego:
1. Reiniciar Odoo
2. Ir a **Aplicaciones > Actualizar Lista de Aplicaciones**
3. Buscar "Token Search"
4. Click en **Instalar**

## 🔄 Futuros Cambios

Para subir cambios nuevos:

```bash
cd /Users/fabrizio/Documents/code/odoov18-enterprise-mundolimpio/addons/aftermoves_token_search

# Ver cambios
git status

# Agregar cambios
git add .

# Commit
git commit -m "Fix: tu descripción del cambio"

# Subir
git push origin main
```

## 🏷️ Crear Releases (Opcional)

Para versiones estables:

1. En GitHub, ve a tu repo
2. Click en **"Releases"** (derecha)
3. Click **"Create a new release"**
4. Tag: `v1.0.0`
5. Title: `Aftermoves Token Search v1.0.0`
6. Descripción: Copiar el Changelog del README
7. Click **"Publish release"**

---

## ✅ Checklist Final

Antes de hacer público:

- [ ] README.md está completo
- [ ] `.gitignore` está configurado
- [ ] Commit message es descriptivo
- [ ] Remote de GitHub está configurado
- [ ] Push exitoso
- [ ] README se ve bien en GitHub
- [ ] Topics agregados
- [ ] Licencia está clara (LGPL-3)

---

**¡Listo!** Tu módulo está en GitHub y listo para compartir. 🎉
