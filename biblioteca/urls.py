from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path,include,re_path
from django.contrib.auth.decorators import login_required
from apps.usuario.views import Inicio,Login,logoutUsuario

urlpatterns = [
    path('automatic-crud/',include('apps.automatic_crud.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]