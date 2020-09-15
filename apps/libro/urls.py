from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('inicio_autor/',InicioAutor.as_view(), name = 'inicio_autor'),
    path('crear_autor/',CrearAutor.as_view(), name = 'crear_autor'),
    path('listado_autor/',ListadoAutor.as_view(), name = 'listar_autor'),
    path('editar_autor/<int:pk>/',ActualizarAutor.as_view(), name = 'editar_autor'),
    path('eliminar_autor/<int:pk>/',EliminarAutor.as_view(), name = 'eliminar_autor'),
    path('inicio_libro/',InicioLibro.as_view(), name = 'inicio_libro'),
    path('listado_libros/', ListadoLibros.as_view(), name = 'listado_libros'),
    path('crear_libro/',CrearLibro.as_view(), name = 'crear_libro'),
    path('editar_libro/<int:pk>/', ActualizarLibro.as_view(), name = 'editar_libro'),
    path('eliminar_libro/<int:pk>/', EliminarLibro.as_view(), name = 'eliminar_libro'),
    # URLS Generales
    path('listar-libros-disponibles/',ListadoLibrosUsuarios.as_view(), name = 'listar_libros_disponibles'),
    path('listar-libros-reservados/',ListadoLibrosReservados.as_view(), name = 'listar_libros_reservados'),
    path('detalle-libro/<int:pk>/',DetalleLibroUsuarios.as_view(), name = 'detalle_libro'),
    path('reservar-libro/',RegistrarReserva.as_view(), name = 'reservar_libro')
]
