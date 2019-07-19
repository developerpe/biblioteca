from django.urls import path
from .views import crearAutor,listarAutor,editarAutor,eliminarAutor,ListadoAutor,ActualizarAutor,CrearAutor,EliminarAutor

urlpatterns = [
    path('crear_autor/',CrearAutor.as_view(), name = 'crear_autor'),
    path('listar_autor/',ListadoAutor.as_view(), name = 'listar_autor'),
    path('editar_autor/<int:pk>',ActualizarAutor.as_view(), name = 'editar_autor'),
    path('eliminar_autor/<int:pk>',EliminarAutor.as_view(), name = 'eliminar_autor')
]
