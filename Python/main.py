# ============================================
# MAIN.PY - Archivo principal de ejecución
# ============================================
#
# Este archivo no contiene la lógica del sistema: su responsabilidad
# es orquestar las piezas. Carga los posts desde el JSON, instancia
# la clase Blog, y coordina el flujo del menú llamando a los métodos
# de esa instancia.

from blog.datos import cargar_posts, guardar_posts
from blog.modelos import Autor, Post, Blog, ESTADOS_POST
from blog.menu import mostrar_menu, pedir_datos_nuevo_post


def main():
    # Al iniciar el programa, leemos los posts existentes desde
    # posts.json y armamos la instancia de Blog con esos datos.
    posts = cargar_posts()
    blog = Blog(posts)

    activo = True

    while activo:
        opcion = mostrar_menu()

        # Si mostrar_menu() devolvió None, fue porque el input no era
        # un número válido; el mensaje de error ya se mostró ahí adentro.
        if opcion is None:
            continue

        if opcion == 1:
            blog.listar_posts()

        elif opcion == 2:
            termino = input("Ingresá el título (o parte) a buscar: ")
            blog.buscar_por_titulo(termino)

        elif opcion == 3:
            tag = input("Ingresá el tag a filtrar: ")
            blog.filtrar_por_tag(tag)

        elif opcion == 4:
            blog.validar_posts()

        elif opcion == 5:
            datos_ingresados = pedir_datos_nuevo_post(ESTADOS_POST)

            nuevo_autor = Autor(
                nombre=datos_ingresados["nombre_autor"],
                bio=datos_ingresados["bio_autor"],
            )
            nuevo_post = Post(
                id=blog.siguiente_id(),
                titulo=datos_ingresados["titulo"],
                contenido=datos_ingresados["contenido"],
                autor=nuevo_autor,
                tags=datos_ingresados["tags"],
                estado=datos_ingresados["estado"],
            )

            blog.agregar_post(nuevo_post)
            # Convertimos toda la lista (incluido el post nuevo) a
            # diccionarios y la guardamos en posts.json.
            guardar_posts(blog.posts)
            print(f"Post '{nuevo_post.titulo}' agregado y guardado en posts.json.")

        elif opcion == 6:
            print("¡Gracias por usar el sistema de blog! Hasta luego.")
            activo = False

        else:
            print("Opción inválida, intenta de nuevo")


if __name__ == "__main__":
    main()
