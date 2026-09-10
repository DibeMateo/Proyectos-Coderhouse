# ============================================
# OPERACIONES.PY - Operaciones principales del blog
# ============================================
#
# Contiene las funciones que trabajan sobre la lista de posts:
# listar, buscar por título y filtrar por tag. Reciben los datos
# por parámetro (no dependen de variables globales), para que puedan
# reutilizarse con cualquier lista de posts que se les pase.


def listar_posts(lista):
    """
    Recorre la lista de posts y muestra, para cada uno, el título,
    el nombre del autor (accediendo al diccionario anidado 'autor')
    y el estado del post.
    """
    if not lista:
        print("No hay posts para mostrar.")
        return

    print("\n--- LISTA DE POSTS ---")
    for post in lista:
        # Usamos .get() para no romper el programa si falta alguna clave
        titulo = post.get("titulo", "(sin título)")
        autor = post.get("autor")
        estado = post.get("estado", "(sin estado)")

        # El autor puede venir mal cargado (ej: texto simple en vez de dict),
        # así que verificamos con isinstance antes de acceder a ['nombre']
        if isinstance(autor, dict):
            nombre_autor = autor.get("nombre", "(autor sin nombre)")
        else:
            nombre_autor = "(autor inválido)"

        print(f"- {titulo} | Autor: {nombre_autor} | Estado: {estado}")


def buscar_por_titulo(lista, termino):
    """
    Busca posts cuyo título contenga 'termino', ignorando mayúsculas/minúsculas.
    Recibe la lista de posts y el término de búsqueda.
    Retorna la lista de coincidencias (para que quien llame decida qué hacer).
    """
    # Si el usuario no escribió nada, avisamos y no seguimos buscando
    if not termino.strip():
        print("No ingresaste ningún término de búsqueda.")
        return []

    termino = termino.lower()
    resultados = []

    for post in lista:
        titulo = post.get("titulo", "")
        # Nos aseguramos de que titulo sea string antes de usar .lower()
        if isinstance(titulo, str) and termino in titulo.lower():
            resultados.append(post)

    if resultados:
        print(f"\n--- RESULTADOS PARA '{termino}' ---")
        for post in resultados:
            print(f"- {post.get('titulo', '(sin título)')}")
    else:
        print(f"No se encontraron posts con '{termino}' en el título.")

    return resultados


def filtrar_por_tag(lista, tag):
    """
    Filtra los posts que tengan 'tag' dentro de su lista de tags.
    Ignora mayúsculas/minúsculas. Recibe la lista y el tag a buscar.
    Retorna la lista de posts que matchean.
    """
    # Si el usuario no escribió nada, avisamos y no seguimos filtrando
    if not tag.strip():
        print("No ingresaste ningún tag para filtrar.")
        return []

    tag = tag.lower()
    resultados = []

    for post in lista:
        tags_post = post.get("tags", [])
        # Si tags no es una lista (ej: quedó cargado como string), lo salteamos
        if not isinstance(tags_post, list):
            continue

        tags_normalizados = [t.lower() for t in tags_post if isinstance(t, str)]
        if tag in tags_normalizados:
            resultados.append(post)

    if resultados:
        print(f"\n--- POSTS CON TAG '{tag}' ---")
        for post in resultados:
            print(f"- {post.get('titulo', '(sin título)')} (tags: {post.get('tags')})")
    else:
        print(f"No se encontraron posts con el tag '{tag}'.")

    return resultados
