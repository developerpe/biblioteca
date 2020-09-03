from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path,include,re_path
from django.contrib.auth.decorators import login_required
from apps.usuario.views import Inicio,Login,logoutUsuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/',include(('apps.usuario.urls','usuarios'))),
    path('libro/',include(('apps.libro.urls','libro'))),
    path('',Inicio.as_view(), name = 'index'),
    path('accounts/login/',Login.as_view(), name = 'login'),
    path('logout/',login_required(logoutUsuario),name = 'logout'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]