# Blog Project (Django)

Proyecto base de un blog desarrollado con Django. Incluye la app `posts`,
configurada en español y con la zona horaria de Argentina, lista como punto
de partida para agregar modelos, vistas y templates en los próximos módulos.

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

## Estructura del proyecto
