# ============================================
# DATOS.PY - Persistencia en JSON
# ============================================
#
# Este módulo se encarga de leer y escribir los posts en el archivo
# posts.json, usando el módulo json de Python. Trabaja siempre con
# objetos Post/Autor hacia el resto del programa: la conversión a
# diccionario (para poder guardarlos en JSON) y la reconstrucción
# desde diccionario (al leerlos) ocurre acá, usando post.to_dict()
# y Post.from_dict() de modelos.py.

import json
import os

from .modelos import Autor, Post

# Ubicamos posts.json en la raíz del proyecto (un nivel arriba de blog/),
# sin importar desde qué carpeta se ejecute python main.py.
_CARPETA_BLOG = os.path.dirname(os.path.abspath(__file__))
_CARPETA_RAIZ = os.path.dirname(_CARPETA_BLOG)
RUTA_JSON = os.path.join(_CARPETA_RAIZ, "posts.json")


def _datos_iniciales():
    """Datos semilla, usados solo la primera vez que se ejecuta el
    programa (si posts.json todavía no existe). Incluye un post con
    datos incompletos/incorrectos a propósito, para poder probar
    validar_post()."""
    autor_1 = Autor(nombre="Mateo Di Benedetto", bio="Analista de datos y programador")
    autor_2 = Autor(nombre="Lucía Fernández", bio="Redactora de contenido técnico")

    return [
        Post(
            id=1,
            titulo="Introducción a Python",
            contenido="Python es un lenguaje versátil y fácil de aprender.",
            autor=autor_1,
            tags=["python", "datos"],
            estado="publicado",
        ),
        Post(
            id=2,
            titulo="Modelos en Django",
            contenido="Los modelos representan las tablas de la base de datos.",
            autor=autor_2,
            tags=["django", "python"],
            estado="publicado",
        ),
        Post(
            id=3,
            titulo="Consultas SQL básicas",
            contenido="SELECT, WHERE y JOIN son la base para consultar datos.",
            autor=autor_1,
            tags=["sql", "datos"],
            estado="borrador",
        ),
        Post(
            # Post INVÁLIDO a propósito:
            # - titulo vacío
            # - autor como texto simple, no como instancia de Autor
            # - tags como string en vez de lista
            # - estado que no pertenece a ESTADOS_POST
            id=4,
            titulo="",
            contenido="Contenido de prueba con datos incorrectos.",
            autor="Autor Desconocido",
            tags="powerbi",
            estado="eliminado",
        ),
    ]


def cargar_posts():
    """
    Lee los posts desde posts.json y los devuelve como una lista de
    objetos Post (con su Autor anidado ya reconstruido).

    Si el archivo todavía no existe (primera ejecución del programa),
    se crea con datos semilla y se guarda, para que el sistema tenga
    algo con qué trabajar desde el primer momento.
    """
    if not os.path.exists(RUTA_JSON):
        posts_iniciales = _datos_iniciales()
        guardar_posts(posts_iniciales)
        return posts_iniciales

    with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
        datos_crudos = json.load(archivo)

    return [Post.from_dict(item) for item in datos_crudos]


def guardar_posts(posts):
    """
    Recibe una lista de objetos Post, los convierte a diccionarios
    (con post.to_dict(), que a su vez convierte el Autor anidado con
    autor.to_dict()) y los escribe en posts.json usando el módulo json.
    """
    datos_serializados = [post.to_dict() for post in posts]

    with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos_serializados, archivo, ensure_ascii=False, indent=2)
