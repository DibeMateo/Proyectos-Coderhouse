# Sistema de Blog por Consola

Sistema interactivo de blog que se maneja desde la terminal, organizado en
clases (Programación Orientada a Objetos), módulos y paquetes de Python,
con persistencia de datos en un archivo JSON.

Este proyecto es la evolución del sistema de blog desarrollado en los
módulos anteriores: estructuras de datos → sistema interactivo →
refactorización con funciones → organización en módulos y paquetes →
**modelado con clases y persistencia en JSON** (este entregable).

## Qué hace el programa

Al iniciar, carga los posts existentes desde `posts.json` (si el archivo
no existe todavía, lo crea automáticamente con datos de ejemplo). Después
muestra un menú con 6 opciones:

```
--- MENU DEL BLOG ---
1. Ver todos los posts
2. Buscar por titulo
3. Filtrar por tag
4. Validar posts
5. Agregar nuevo post
6. Salir
```

- **Ver todos los posts**: muestra título, autor y estado de cada post.
- **Buscar por título**: busca coincidencias (parciales, sin distinguir
  mayúsculas/minúsculas) en el título de los posts.
- **Filtrar por tag**: muestra los posts que tengan una etiqueta específica.
- **Validar posts**: recorre todos los posts cargados y muestra cuáles
  cumplen con las reglas de negocio y cuáles tienen errores (por ejemplo,
  título vacío, autor mal formado, tags con tipo de dato incorrecto o
  estado inválido).
- **Agregar nuevo post**: pide los datos por consola, crea los objetos
  `Autor` y `Post` correspondientes, los agrega al blog en memoria y
  **guarda inmediatamente los cambios en `posts.json`**.
- **Salir**: muestra un mensaje de despedida y termina la ejecución.

El programa maneja entradas inválidas sin cerrarse inesperadamente: texto
en lugar de un número, opciones fuera de rango, búsquedas o filtros vacíos.

## Cómo ejecutarlo

Requiere Python 3 (no usa librerías externas, todo es de la librería
estándar). Desde la carpeta raíz del proyecto (`blog_consola/`), ejecutar:

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
├── posts.json
├── .gitignore
└── blog/
    ├── __init__.py
    ├── modelos.py
    ├── datos.py
    ├── menu.py
    └── validaciones.py
```

## Qué responsabilidad cumple cada módulo

| Archivo                | Responsabilidad                                                        |
|-------------------------|--------------------------------------------------------------------------|
| `main.py`               | Orquesta el sistema: carga los posts, instancia `Blog` y coordina el flujo del menú llamando a los métodos de esa instancia. No contiene lógica de negocio propia. |
| `blog/__init__.py`      | Permite que Python reconozca `blog/` como un paquete. Está vacío.       |
| `blog/modelos.py`       | Define las clases `Autor`, `Post` y `Blog`. `Blog` centraliza la lógica del sistema (listar, buscar, filtrar, agregar, validar) y contiene la lista de objetos `Post`. |
| `blog/datos.py`         | Se encarga exclusivamente de la persistencia: lee y escribe `posts.json` usando el módulo `json` de Python. |
| `blog/menu.py`          | Muestra el menú, captura la opción del usuario con `input()` (con `try/except`), y pide los datos de un post nuevo. Solo interfaz de consola, sin lógica de negocio. |
| `blog/validaciones.py`  | Contiene `validar_post`, con las reglas de negocio que debe cumplir cada objeto `Post`. |

## Cómo interactúan las clases con el archivo JSON

1. **Al iniciar el programa** (`main.py`), se llama a `cargar_posts()` en
   `blog/datos.py`. Esta función lee `posts.json`, y por cada diccionario
   que encuentra en el archivo, llama a `Post.from_dict(...)` — que a su
   vez reconstruye el `Autor` anidado con `Autor.from_dict(...)`. El
   resultado es una lista de **objetos** `Post` (no diccionarios sueltos),
   con la que se instancia la clase `Blog`.

2. **Durante la ejecución**, el menú llama a los métodos de esa instancia
   de `Blog` (`blog.listar_posts()`, `blog.buscar_por_titulo(...)`,
   `blog.filtrar_por_tag(...)`, `blog.validar_posts()`), que trabajan
   directamente sobre los objetos `Post` en memoria.

3. **Al crear un post nuevo** (opción 5), se arma un objeto `Autor` y un
   objeto `Post` con los datos ingresados, se agregan a `blog.posts` con
   `blog.agregar_post(...)`, y **inmediatamente** se llama a
   `guardar_posts(blog.posts)` en `blog/datos.py`. Esa función convierte
   cada objeto `Post` (y su `Autor` anidado) a diccionario con
   `post.to_dict()`, y escribe la lista completa en `posts.json` con
   `json.dump(...)`. Así, la próxima vez que se ejecute el programa, ese
   post ya va a estar ahí.

4. **Un dato de prueba inválido**: entre los datos iniciales hay un post
   con el título vacío, el autor cargado como texto simple (en vez de un
   objeto `Autor`) y un estado que no existe. Sirve para comprobar que
   `validar_post()` detecta correctamente esos errores, sin que el
   programa se rompa al leerlo o mostrarlo.

## Qué archivo se debe ejecutar

Únicamente `main.py`, desde la carpeta raíz del proyecto (`blog_consola/`).
Los archivos dentro de `blog/` no están pensados para ejecutarse de forma
independiente: son módulos que `main.py` importa.
