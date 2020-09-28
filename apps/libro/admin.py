from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Autor,Libro,Reserva
from .forms import ReservaForm

class ReservaAdmin(admin.ModelAdmin):
    form = ReservaForm
    list_display = ('libro','usuario','fecha_creacion','estado')

class AutorResource(resources.ModelResource):
    class Meta:
        model = Autor

class AutorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ('nombre','apellidos','nacionalidad')
    list_display = ('nombre','apellidos','nacionalidad','estado')
    resource_class = AutorResource
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
admin.site.register(Reserva,ReservaAdmin)
