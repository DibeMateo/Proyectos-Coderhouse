# ============================================
# DATOS.PY - Estructuras de datos base del blog
# ============================================
#
# Este módulo NO contiene lógica de negocio ni interacción con el usuario.
# Su única responsabilidad es definir y exponer los datos con los que
# trabaja el resto del sistema.

# --- Perfiles de autor (diccionarios) ---

perfil_autor = {
    "nombre": "Mateo Di Benedetto",
    "email": "mateo@example.com",
    "bio": "Analista de datos y programador"
}

perfil_autor_2 = {
    "nombre": "Lucía Fernández",
    "email": "lucia@example.com",
    "bio": "Redactora de contenido técnico"
}

# Tupla con los estados válidos de un post (inmutable)
estados_post = ("borrador", "publicado", "archivado")

# Set con las etiquetas disponibles en el blog
etiquetas_blog = {"python", "django", "sql", "powerbi", "datos"}

# Lista de posts. A propósito, dejamos al menos uno con datos
# incompletos/incorrectos para poder probar validar_post().
posts = [
    {
        "id": 1,
        "titulo": "Introducción a Python",
        "contenido": "Python es un lenguaje versátil y fácil de aprender.",
        "autor": perfil_autor,
        "tags": ["python", "datos"],
        "estado": "publicado"
    },
    {
        "id": 2,
        "titulo": "Modelos en Django",
        "contenido": "Los modelos representan las tablas de la base de datos.",
        "autor": perfil_autor_2,
        "tags": ["django", "python"],
        "estado": "publicado"
    },
    {
        "id": 3,
        "titulo": "Consultas SQL básicas",
        "contenido": "SELECT, WHERE y JOIN son la base para consultar datos.",
        "autor": perfil_autor,
        "tags": ["sql", "datos"],
        "estado": "borrador"
    },
    {
        # Post INVÁLIDO a propósito, para probar validar_post():
        # - titulo vacío
        # - autor como texto simple, no como diccionario
        # - tags como string en vez de lista
        # - estado que no pertenece a estados_post
        "id": 4,
        "titulo": "",
        "contenido": "Contenido de prueba con datos incorrectos.",
        "autor": "Autor Desconocido",
        "tags": "powerbi",
        "estado": "eliminado"
    },
]
