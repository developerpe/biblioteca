from django.urls import path
from .views import crearAutor,listarAutor,editarAutor,eliminarAutor,ListadoAutor

urlpatterns = [
    path('crear_autor/',crearAutor, name = 'crear_autor'),
    path('listar_autor/',ListadoAutor.as_view(), name = 'listar_autor'),
    path('editar_autor/<int:id>',editarAutor, name = 'editar_autor'),
    path('eliminar_autor/<int:id>',eliminarAutor, name = 'eliminar_autor')
]
