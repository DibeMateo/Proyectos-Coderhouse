# ============================================
# VALIDACIONES.PY - Reglas lógicas del sistema
# ============================================
#
# Verifica que un objeto Post cumpla con las reglas de negocio
# esperadas. No imprime en consola directamente ni maneja el menú:
# solo valida y retorna resultados, para que quien lo use (la clase
# Blog) decida qué hacer con esa información.

from .modelos import Autor, Post, ESTADOS_POST


def validar_post(post):
    """
    Verifica que un objeto Post cumpla con las reglas de negocio esperadas.
    Retorna una tupla (True, "OK") si es válido, o (False, "mensaje de error") si no.
    """
    # 1. El post debe ser una instancia de la clase Post
    if not isinstance(post, Post):
        return False, "El post no es una instancia de la clase Post."

    # 2. El título no debe estar vacío
    if not post.titulo:
        return False, "El título está vacío."

    # 3. El contenido no debe estar vacío
    if not post.contenido:
        return False, "El contenido está vacío."

    # 4. El autor debe ser una instancia de Autor
    if not isinstance(post.autor, Autor):
        return False, "El campo 'autor' no es una instancia de Autor."

    # 5. El autor debe tener nombre
    if not getattr(post.autor, "nombre", None):
        return False, "El autor no tiene nombre."

    # 6. Tags debe ser una lista
    if not isinstance(post.tags, list):
        return False, "El campo 'tags' no es una lista."

    # 7. El estado debe ser uno de los valores definidos en ESTADOS_POST
    if post.estado not in ESTADOS_POST:
        return False, f"El estado '{post.estado}' no es válido."

    # Si pasó todas las validaciones, el post es correcto
    return True, "OK"
