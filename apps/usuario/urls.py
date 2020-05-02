from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.usuario.views import ListadoUsuario,RegistrarUsuario

urlpatterns = [
    path('listado_usuarios/', login_required(ListadoUsuario.as_view()),
         name='listar_usuarios'),
    path('registrar_usuario/',login_required(RegistrarUsuario.as_view()),name = 'registrar_usuario'),
]
