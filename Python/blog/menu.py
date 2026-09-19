# ============================================
# MENU.PY - Menú e interacción con el usuario
# ============================================
#
# Este módulo se encarga exclusivamente de mostrar las opciones
# disponibles y capturar la entrada del usuario mediante input().
# No contiene lógica de negocio ni de persistencia: solo interfaz
# de consola.


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
    print("5. Agregar nuevo post")
    print("6. Salir")

    try:
        opcion = int(input("Elegí una opción: "))
        return opcion
    except ValueError:
        # El usuario escribió algo que no es un número
        print("Opción inválida, intenta de nuevo (debe ser un número).")
        return None


def pedir_datos_nuevo_post(estados_validos):
    """
    Pide por consola los datos necesarios para crear un post nuevo.
    Retorna un diccionario con los datos crudos ingresados por el
    usuario (todavía sin convertir a objetos Post/Autor - eso lo
    hace quien llama a esta función).
    """
    print("\n--- NUEVO POST ---")
    titulo = input("Título: ")
    contenido = input("Contenido: ")
    nombre_autor = input("Nombre del autor: ")
    bio_autor = input("Bio del autor (opcional): ")
    tags_texto = input("Tags separados por coma (ej: python,django): ")
    tags = [t.strip() for t in tags_texto.split(",") if t.strip()]

    estado = input(f"Estado {estados_validos}: ").strip().lower()
    if estado not in estados_validos:
        print(f"Estado no reconocido, se usará '{estados_validos[0]}' por defecto.")
        estado = estados_validos[0]

    return {
        "titulo": titulo,
        "contenido": contenido,
        "nombre_autor": nombre_autor,
        "bio_autor": bio_autor,
        "tags": tags,
        "estado": estado,
    }
