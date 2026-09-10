# Sistema de Blog por Consola

Sistema interactivo de blog que se maneja desde la terminal, organizado en
módulos y paquetes de Python. Permite listar posts, buscar por título,
filtrar por tag y validar la estructura de los posts cargados en memoria.

Este proyecto es la evolución modularizada del sistema de blog desarrollado
en los módulos anteriores (estructuras de datos → sistema interactivo →
refactorización con funciones → organización en módulos y paquetes).

## Qué hace el programa

Muestra un menú con 5 opciones:

```
--- MENU DEL BLOG ---
1. Ver todos los posts
2. Buscar por titulo
3. Filtrar por tag
4. Validar posts
5. Salir
```

- **Ver todos los posts**: muestra título, autor y estado de cada post.
- **Buscar por título**: busca coincidencias (parciales, sin distinguir
  mayúsculas/minúsculas) en el título de los posts.
- **Filtrar por tag**: muestra los posts que tengan una etiqueta específica.
- **Validar posts**: recorre todos los posts cargados y muestra cuáles
  cumplen con las reglas de negocio y cuáles tienen errores (por ejemplo,
  título vacío, autor mal formado, tags con tipo de dato incorrecto o
  estado inválido).
- **Salir**: muestra un mensaje de despedida y termina la ejecución.

El programa maneja entradas inválidas sin cerrarse inesperadamente: texto
en lugar de un número, opciones fuera de rango, búsquedas o filtros vacíos.

## Cómo ejecutarlo

Requiere Python 3. Desde la carpeta raíz del proyecto (`blog_consola/`),
ejecutar:

```bash
python main.py
```

o, según cómo esté configurado el entorno:

```bash
python3 main.py
```

## Cómo está organizada la carpeta

```
blog_consola/
├── main.py
├── README.md
└── blog/
    ├── __init__.py
    ├── datos.py
    ├── menu.py
    ├── operaciones.py
    └── validaciones.py
```

## Qué responsabilidad cumple cada módulo

| Archivo                | Responsabilidad                                                        |
|-------------------------|--------------------------------------------------------------------------|
| `main.py`               | Orquesta el sistema: importa desde `blog/` y coordina el flujo del menú. No contiene lógica de negocio propia. |
| `blog/__init__.py`      | Permite que Python reconozca `blog/` como un paquete. Está vacío.       |
| `blog/datos.py`         | Define las estructuras de datos base: `perfil_autor`, `estados_post`, `etiquetas_blog` y `posts`. |
| `blog/menu.py`          | Muestra el menú y captura la opción del usuario con `input()`, usando `try/except` para evitar errores por entradas no numéricas. |
| `blog/operaciones.py`   | Contiene `listar_posts`, `buscar_por_titulo` y `filtrar_por_tag`. Reciben los datos por parámetro, sin depender de variables globales. |
| `blog/validaciones.py`  | Contiene `validar_post` y `validar_todos_los_posts`, con las reglas de negocio que debe cumplir cada post. |

## Qué archivo se debe ejecutar

Únicamente `main.py`, desde la carpeta raíz del proyecto (`blog_consola/`).
Los archivos dentro de `blog/` no están pensados para ejecutarse de forma
independiente: son módulos que `main.py` importa.
