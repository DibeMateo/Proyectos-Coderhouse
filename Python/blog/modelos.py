# ============================================
# MODELOS.PY - Clases del sistema (POO)
# ============================================
#
# Este módulo define las 3 clases principales del blog:
# - Autor: representa a la persona que escribe un post.
# - Post: representa una publicación, con un Autor asociado.
# - Blog: centraliza la lógica del sistema; contiene la lista de Posts
#   y los métodos para listar, buscar, filtrar, agregar y validar.
#
# Las clases Autor y Post saben convertirse a diccionario (to_dict) y
# reconstruirse desde uno (from_dict), que es lo que permite guardarlas
# y leerlas del archivo JSON en datos.py.

# Constantes de negocio (antes vivían en datos.py; ahora que datos.py
# pasa a ser el módulo de persistencia JSON, las movemos acá, junto a
# las clases que las usan).
ESTADOS_POST = ("borrador", "publicado", "archivado")
ETIQUETAS_BLOG = {"python", "django", "sql", "powerbi", "datos"}


class Autor:
    """Representa al autor de uno o más posts."""

    def __init__(self, nombre, bio=""):
        self.nombre = nombre
        self.bio = bio

    def to_dict(self):
        """Convierte el objeto Autor a un diccionario, para poder
        guardarlo en JSON con el módulo json de Python."""
        return {
            "nombre": self.nombre,
            "bio": self.bio,
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruye un objeto Autor a partir de un diccionario
        (por ejemplo, uno leído desde el archivo JSON)."""
        return cls(
            nombre=data.get("nombre", ""),
            bio=data.get("bio", ""),
        )

    def __str__(self):
        return self.nombre


class Post:
    """Representa una publicación del blog. Contiene una instancia
    de Autor (no un texto suelto), tal como se venía trabajando en
    los módulos anteriores."""

    def __init__(self, id, titulo, contenido, autor, tags=None, estado="borrador"):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.autor = autor  # instancia de Autor (o dato inválido, a propósito)
        self.tags = tags if tags is not None else []
        self.estado = estado

    def to_dict(self):
        """Convierte el post (y su autor anidado) a un diccionario
        compatible con JSON."""
        # Si el autor es una instancia válida de Autor, lo convertimos
        # también; si vino mal cargado (dato de prueba inválido), lo
        # dejamos tal cual para no perder esa información al guardar.
        if isinstance(self.autor, Autor):
            autor_serializado = self.autor.to_dict()
        else:
            autor_serializado = self.autor

        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": autor_serializado,
            "tags": self.tags,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruye un objeto Post a partir de un diccionario.
        Si 'autor' es un diccionario, lo convierte en un objeto Autor;
        si no (dato incorrecto a propósito, como un texto simple),
        lo deja como está para que validar_post() pueda detectarlo."""
        autor_data = data.get("autor")
        if isinstance(autor_data, dict):
            autor = Autor.from_dict(autor_data)
        else:
            autor = autor_data

        return cls(
            id=data.get("id"),
            titulo=data.get("titulo", ""),
            contenido=data.get("contenido", ""),
            autor=autor,
            tags=data.get("tags", []),
            estado=data.get("estado", ""),
        )

    def __str__(self):
        return self.titulo


class Blog:
    """Centraliza la lógica del sistema. Contiene la lista de posts
    (objetos Post) y los métodos para operar sobre ellos."""

    def __init__(self, posts=None):
        self.posts = posts if posts is not None else []

    def agregar_post(self, post):
        """Agrega un nuevo Post a la lista en memoria."""
        self.posts.append(post)

    def listar_posts(self):
        """Muestra título, autor y estado de cada post."""
        if not self.posts:
            print("No hay posts para mostrar.")
            return

        print("\n--- LISTA DE POSTS ---")
        for post in self.posts:
            nombre_autor = post.autor.nombre if isinstance(post.autor, Autor) else "(autor inválido)"
            print(f"- {post.titulo or '(sin título)'} | Autor: {nombre_autor} | Estado: {post.estado or '(sin estado)'}")

    def buscar_por_titulo(self, termino):
        """Busca posts cuyo título contenga 'termino' (sin distinguir
        mayúsculas/minúsculas). Retorna la lista de coincidencias."""
        if not termino.strip():
            print("No ingresaste ningún término de búsqueda.")
            return []

        termino = termino.lower()
        resultados = [
            post for post in self.posts
            if isinstance(post.titulo, str) and termino in post.titulo.lower()
        ]

        if resultados:
            print(f"\n--- RESULTADOS PARA '{termino}' ---")
            for post in resultados:
                print(f"- {post.titulo}")
        else:
            print(f"No se encontraron posts con '{termino}' en el título.")

        return resultados

    def filtrar_por_tag(self, tag):
        """Filtra los posts que tengan 'tag' entre sus etiquetas (sin
        distinguir mayúsculas/minúsculas). Retorna la lista de coincidencias."""
        if not tag.strip():
            print("No ingresaste ningún tag para filtrar.")
            return []

        tag = tag.lower()
        resultados = []
        for post in self.posts:
            if not isinstance(post.tags, list):
                continue
            tags_normalizados = [t.lower() for t in post.tags if isinstance(t, str)]
            if tag in tags_normalizados:
                resultados.append(post)

        if resultados:
            print(f"\n--- POSTS CON TAG '{tag}' ---")
            for post in resultados:
                print(f"- {post.titulo} (tags: {post.tags})")
        else:
            print(f"No se encontraron posts con el tag '{tag}'.")

        return resultados

    def validar_posts(self):
        """Recorre todos los posts y muestra cuáles son válidos y
        cuáles tienen errores, usando validar_post() de validaciones.py."""
        # Import local (dentro del método) para evitar un import circular:
        # validaciones.py importa Autor/Post/ESTADOS_POST desde este mismo
        # módulo, así que si importáramos validaciones.py arriba de todo
        # (a nivel de módulo), Python encontraría un ciclo. Importándolo
        # acá adentro, para cuando se llama a este método ambos módulos
        # ya están completamente cargados y el ciclo no es un problema.
        from .validaciones import validar_post

        print("\n--- VALIDACIÓN DE POSTS ---")
        for post in self.posts:
            es_valido, mensaje = validar_post(post)
            if es_valido:
                print(f"Post {post.id}: OK")
            else:
                print(f"Post {post.id}: INVÁLIDO -> {mensaje}")

    def siguiente_id(self):
        """Calcula el próximo id disponible, para asignarlo a un post nuevo."""
        ids_validos = [post.id for post in self.posts if isinstance(post.id, int)]
        return max(ids_validos, default=0) + 1
