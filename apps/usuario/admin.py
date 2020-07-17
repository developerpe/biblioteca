from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.usuario.models import Usuario

admin.site.register(Usuario)
admin.site.register(Permission)
admin.site.register(ContentType)
