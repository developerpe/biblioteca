from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import crearAutor,listarAutor,editarAutor,eliminarAutor,ListadoAutor,ActualizarAutor,CrearAutor,EliminarAutor

urlpatterns = [
    path('crear_autor/',login_required(CrearAutor.as_view()), name = 'crear_autor'),
    path('listar_autor/',login_required(ListadoAutor.as_view()), name = 'listar_autor'),
    path('editar_autor/<int:pk>',login_required(ActualizarAutor.as_view()), name = 'editar_autor'),
    path('eliminar_autor/<int:pk>',login_required(EliminarAutor.as_view()), name = 'eliminar_autor')
]
