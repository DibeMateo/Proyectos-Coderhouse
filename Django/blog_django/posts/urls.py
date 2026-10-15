from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acerca/', views.acerca, name='acerca'),
    path('posts/', views.lista_posts, name='lista_posts'),
    path('posts/nuevo/', views.crear_post, name='crear_post'),
    path('posts/<int:pk>/', views.detalle_post, name='detalle_post'),
    path('posts/<int:pk>/editar/', views.editar_post, name='editar_post'),
    path('posts/<int:pk>/eliminar/', views.eliminar_post, name='eliminar_post'),
]
