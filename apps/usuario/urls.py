from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from apps.usuario.views import ListadoUsuario, RegistrarUsuario

urlpatterns = [
    path('listado_usuarios/', login_required(ListadoUsuario.as_view()),{'parametro_extra': 'Hola!'},name='listar_usuarios'),
    path('registrar_usuario/',login_required(RegistrarUsuario.as_view()),name = 'registrar_usuario'),
]

#URLS DE VISTAS IMPLICITAS
urlpatterns += [
    path('inicio_usuarios/', login_required(
        TemplateView.as_view(
            template_name='usuarios/listar_usuario.html'
        )
    ), name='inicio_usuarios'),
]
