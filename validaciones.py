# ============================================
# VALIDACIONES.PY - Reglas lógicas del sistema
# ============================================
#
# Este módulo se encarga de verificar que los datos (los posts)
# cumplan con las reglas de negocio esperadas. No imprime en consola
# directamente ni maneja el menú: solo valida y retorna resultados,
# para que quien lo use decida qué hacer con esa información.

from .datos import estados_post


def validar_post(post):
    """
    Verifica que un post cumpla con las reglas de negocio esperadas.
    Retorna una tupla (True, "OK") si es válido, o (False, "mensaje de error") si no.
    """
    claves_obligatorias = ["id", "titulo", "contenido", "autor", "tags", "estado"]

    # 1. El post debe ser un diccionario
    if not isinstance(post, dict):
        return False, "El post no es un diccionario."

    # 2. Deben existir todas las claves obligatorias
    for clave in claves_obligatorias:
        if clave not in post:
            return False, f"Falta la clave obligatoria '{clave}'."

    # 3. El título no debe estar vacío
    if not post.get("titulo"):
        return False, "El título está vacío."

    # 4. El contenido no debe estar vacío
    if not post.get("contenido"):
        return False, "El contenido está vacío."

    # 5. El autor debe ser un diccionario
    autor = post.get("autor")
    if not isinstance(autor, dict):
        return False, "El campo 'autor' no es un diccionario."

    # 6. El autor debe tener la clave 'nombre'
    if "nombre" not in autor:
        return False, "El autor no tiene la clave 'nombre'."

    # 7. Tags debe ser una lista
    if not isinstance(post.get("tags"), list):
        return False, "El campo 'tags' no es una lista."

    # 8. El estado debe ser uno de los valores válidos definidos en estados_post
    if post.get("estado") not in estados_post:
        return False, f"El estado '{post.get('estado')}' no es válido."

    # Si pasó todas las validaciones, el post es correcto
    return True, "OK"


def validar_todos_los_posts(lista):
    """
    Recorre la lista de posts y usa validar_post() sobre cada uno,
    mostrando cuáles son válidos y cuáles tienen errores.
    """
    print("\n--- VALIDACIÓN DE POSTS ---")
    for post in lista:
        es_valido, mensaje = validar_post(post)
        identificador = post.get("id", "?") if isinstance(post, dict) else "?"

        if es_valido:
            print(f"Post {identificador}: OK")
        else:
            print(f"Post {identificador}: INVÁLIDO -> {mensaje}")
