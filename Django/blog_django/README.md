# Blog Project (Django)

Proyecto base de un blog desarrollado con Django. Incluye la app `posts`,
configurada en español y con la zona horaria de Argentina. Ya cuenta con
un sitio navegable (páginas de Inicio y Acerca de), con herencia de
templates y estilos propios en CSS.

## Requisitos previos

- Python 3.10 o superior
- pip

## Cómo clonar el repositorio

```bash
git clone https://github.com/DibeMateo/Proyectos-Coderhouse.git
cd Proyectos-Coderhouse/Django/blog_django
```

## Cómo crear y activar el entorno virtual

Crear el entorno virtual (una sola vez):

```bash
python3 -m venv venv
```

Activarlo (hay que repetir este paso cada vez que abrís una terminal nueva
para trabajar en el proyecto):

- En macOS / Linux:
```bash
  source venv/bin/activate
```
- En Windows:
```bash
  venv\Scripts\activate
```

Vas a ver que el prompt de la terminal cambia, agregando `(venv)` al
principio — esa es la señal de que el entorno está activo.

## Cómo instalar las dependencias

Con el entorno virtual ya activado:

```bash
pip install -r requirements.txt
```

Esto instala Django y el resto de las dependencias con las mismas
versiones exactas con las que fue desarrollado el proyecto.

## Cómo levantar el servidor de desarrollo

```bash
python manage.py runserver
```

El proyecto va a quedar disponible en `http://127.0.0.1:8000/`.

## App principal

La app creada para este proyecto se llama **`posts`**, registrada en
`blog_project/settings.py` dentro de `INSTALLED_APPS` como
`posts.apps.PostsConfig`.

## Páginas disponibles

| Ruta        | Vista              | Template                  |
|-------------|---------------------|----------------------------|
| `/`         | `posts.views.inicio` | `posts/templates/posts/inicio.html` |
| `/acerca/`  | `posts.views.acerca` | `posts/templates/posts/acerca.html` |

Ambos templates heredan de `posts/templates/posts/base.html` mediante
`{% extends %}`, que define el esqueleto HTML común (navegación y hoja
de estilos). Las rutas se declaran en `posts/urls.py` y se conectan al
proyecto principal desde `blog_project/urls.py` con `include()`.

## Archivos estáticos (CSS)

Los estilos viven en `posts/static/posts/css/estilos.css`, y se cargan
en `base.html` con `{% load static %}` y `{% static 'posts/css/estilos.css' %}`.

## Estructura del proyecto

## Base de datos y panel de administración

El proyecto usa SQLite (archivo `db.sqlite3`, que no se sube al repositorio). Después de clonar e instalar las dependencias, hay que crear la base de datos local:

    python manage.py migrate

El modelo `Post` (`posts/models.py`) tiene los campos `titulo`, `contenido`, `autor`, `fecha_creacion` y `estado` (borrador, publicado o archivado).

### Cómo entrar al panel de administración

Primero, crear un superusuario (el comando pide nombre de usuario, email y contraseña):

    python manage.py createsuperuser

Después, levantar el servidor:

    python manage.py runserver

Y entrar a http://127.0.0.1:8000/admin/ con el usuario y la contraseña elegidos. Desde la sección "Posts" se pueden crear, editar y borrar publicaciones.

### Listado de publicaciones

La página http://127.0.0.1:8000/posts/ muestra dinámicamente los posts con estado "publicado", del más reciente al más antiguo. Los posts en borrador o archivados no aparecen.

## CRUD de publicaciones con imágenes

| Ruta | Vista | Descripción |
|---|---|---|
| `/posts/` | `lista_posts` | Lista de publicaciones (solo las "Publicado") |
| `/posts/nuevo/` | `crear_post` | Formulario para crear |
| `/posts/<id>/` | `detalle_post` | Detalle de una publicación |
| `/posts/<id>/editar/` | `editar_post` | Formulario para editar |
| `/posts/<id>/eliminar/` | `eliminar_post` | Confirmación y borrado (solo por POST) |

### Manejo de imágenes

- El modelo `Post` tiene un campo `imagen = ImageField(upload_to='posts/', null=True, blank=True)`. Es opcional.
- `ImageField` requiere **Pillow** (`pip install Pillow`, ya incluido en `requirements.txt`).
- En `settings.py` se definen `MEDIA_URL = '/media/'` y `MEDIA_ROOT = BASE_DIR / 'media'`.
- En `blog_project/urls.py` se usa `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` solo cuando `DEBUG = True` (desarrollo).
- Para subir archivos, el `<form>` necesita `method="post"` y `enctype="multipart/form-data"`, y la vista tiene que pasar `request.FILES` al formulario: `PostForm(request.POST, request.FILES)`.
- Las imágenes se guardan en `media/posts/` y en la base solo se guarda la ruta. En los templates se muestran con `{{ post.imagen.url }}`.
- Para que un post nuevo aparezca en la lista, su estado debe ser "Publicado".
