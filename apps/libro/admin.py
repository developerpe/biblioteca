from django.contrib import admin
from .models import Autor,Libro



class AutorAdmin(admin.ModelAdmin):
    actions = ['eliminacion_logica_autores', 'activacion_logica_autores']

    def eliminacion_logica_autores(self, request, queryset):
        for autor in queryset:
            autor.estado = False
            autor.save()
    
    def activacion_logica_autores(self, request, queryset):
        for autor in queryset:
            autor.estado = True
            autor.save()
    
    def get_actions(self,request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro)
