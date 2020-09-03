from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.urls import reverse_lazy
from apps.usuario.mixins import LoginYSuperStaffMixin, ValidarPermisosMixin
from apps.libro.models import Autor, Libro
from apps.libro.forms import AutorForm,LibroForm


class InicioAutor(LoginYSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    template_name = 'libro/autor/listar_autor.html'
    permission_required = ('libro.view_autor','libro.add_autor',
                            'libro.delete_autor','libro.change_autor')


class ListadoAutor(LoginYSuperStaffMixin, ValidarPermisosMixin, ListView):
    model = Autor
    permission_required = ('libro.view_autor', 'libro.add_autor',
                           'libro.delete_autor', 'libro.change_autor')

    def get_queryset(self):
        return self.model.objects.filter(estado=True)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('libro:inicio_autor')


class ActualizarAutor(LoginYSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/autor.html'
    permission_required = ('libro.view_autor', 'libro.add_autor',
                           'libro.delete_autor', 'libro.change_autor')
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('libro:inicio_autor')


class CrearAutor(LoginYSuperStaffMixin, ValidarPermisosMixin, CreateView):
    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/crear_autor.html'
    permission_required = ('libro.view_autor', 'libro.add_autor',
                           'libro.delete_autor', 'libro.change_autor')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_autor = Autor(
                    nombre=form.cleaned_data.get('nombre'),
                    apellidos=form.cleaned_data.get('apellidos'),
                    nacionalidad=form.cleaned_data.get('nacionalidad'),
                    descripcion=form.cleaned_data.get('descripcion')
                )
                nuevo_autor.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('libro:inicio_autor')


class EliminarAutor(LoginYSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    model = Autor
    template_name = 'libro/autor/eliminar_autor.html'
    permission_required = ('libro.view_autor', 'libro.add_autor',
                           'libro.delete_autor', 'libro.change_autor')

    def delete(self,request,pk,*args,**kwargs):
        if request.is_ajax():
            autor = self.get_object()
            autor.estado = False
            autor.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('libro:listar_autor')


class InicioLibro(LoginYSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    template_name = 'libro/libro/listar_libro.html'
    permission_required = ('libro.view_libro', 'libro.add_libro',
                           'libro.delete_libro', 'libro.change_libro')


class CrearLibro(LoginYSuperStaffMixin, ValidarPermisosMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/crear_libro.html'
    permission_required = ('libro.view_libro', 'libro.add_libro',
                           'libro.delete_libro', 'libro.change_libro')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('libro:inicio_libro')


class ListadoLibros(LoginYSuperStaffMixin, ValidarPermisosMixin, ListView):
    model = Libro
    permission_required = ('libro.view_libro', 'libro.add_libro',
                           'libro.delete_libro', 'libro.change_libro')

    def get_queryset(self):
        return self.model.objects.filter(estado = True)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('libro:inicio_libro')


class ActualizarLibro(LoginYSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/libro.html'
    permission_required = ('libro.view_libro', 'libro.add_libro',
                           'libro.delete_libro', 'libro.change_libro')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES,instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('libro:inicio_libro')


class EliminarLibro(LoginYSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    model = Libro
    template_name = 'libro/libro/eliminar_libro.html'
    permission_required = ('libro.view_libro', 'libro.add_libro',
                           'libro.delete_libro', 'libro.change_libro')

    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            libro = self.get_object()
            libro.estado = False
            libro.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('libro:listar_libro')
