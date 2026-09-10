# ============================================
# MAIN.PY - Archivo principal de ejecución
# ============================================
#
# Este archivo no contiene la lógica del sistema: su responsabilidad
# es orquestar las piezas. Importa los datos y las funciones desde
# el paquete 'blog' y coordina el flujo del menú.

from blog.datos import posts
from blog.menu import mostrar_menu
from blog.operaciones import listar_posts, buscar_por_titulo, filtrar_por_tag
from blog.validaciones import validar_todos_los_posts


def main():
    activo = True

    while activo:
        opcion = mostrar_menu()

        # Si mostrar_menu() devolvió None, fue porque el input no era
        # un número válido; el mensaje de error ya se mostró ahí adentro.
        if opcion is None:
            continue

        if opcion == 1:
            listar_posts(posts)
        elif opcion == 2:
            termino = input("Ingresá el título (o parte) a buscar: ")
            buscar_por_titulo(posts, termino)
        elif opcion == 3:
            tag = input("Ingresá el tag a filtrar: ")
            filtrar_por_tag(posts, tag)
        elif opcion == 4:
            validar_todos_los_posts(posts)
        elif opcion == 5:
            print("¡Gracias por usar el sistema de blog! Hasta luego.")
            activo = False
        else:
            print("Opción inválida, intenta de nuevo")


if __name__ == "__main__":
    main()
