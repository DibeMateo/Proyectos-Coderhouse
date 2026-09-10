# ============================================
# MENU.PY - Menú e interacción con el usuario
# ============================================
#
# Este módulo se encarga exclusivamente de mostrar las opciones
# disponibles y capturar la entrada del usuario mediante input().
# No contiene lógica de negocio: solo interfaz de consola.


def mostrar_menu():
    """
    Muestra el menú principal y captura la opción del usuario.
    Usa try/except para evitar que el programa se caiga si el
    usuario ingresa texto en lugar de un número.
    Retorna la opción elegida como entero, o None si la entrada es inválida.
    """
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Validar posts")
    print("5. Salir")

    try:
        opcion = int(input("Elegí una opción: "))
        return opcion
    except ValueError:
        # El usuario escribió algo que no es un número
        print("Opción inválida, intenta de nuevo (debe ser un número).")
        return None
