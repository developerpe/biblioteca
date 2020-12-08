from time import time
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView,DetailView
from django.urls import reverse_lazy
from apps.usuario.mixins import LoginYSuperStaffMixin, ValidarPermisosMixin,LoginMixin
from apps.usuario.models import Usuario
from apps.libro.models import Autor, Libro,Reserva
from apps.libro.forms import AutorForm,LibroForm


class InicioAutor(LoginYSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    template_name = 'libro/autor/listar_autor.html'
    permission_required = ('libro.view_autor','libro.add_autor',
                            'libro.delete_autor','libro.change_autor')

    def get(self,request,*args,**kwargs):
        # METODO 1        
        autores = Autor.objects.all()
        tiempo_inicial = time()
        for index,autor in enumerate(autores,10):
            autor.descripcion = f'Descripcion editada con metodo {index}'
            autor.save()
        tiempo_final = time() - tiempo_inicial
        print(f'Tiempo de Ejecución de método 1: {tiempo_final}')
        
        # METODO 2        
        tiempo_inicial = time()
        for index,autor in enumerate(autores,10):
            autor.descripcion = f'Descripcion editada con metodo {index}'

        for autor in autores:
            autor.save()
        tiempo_final = time() - tiempo_inicial
        print(f'Tiempo de Ejecución de método 2: {tiempo_final}')

        # METODO 3
        """
        tiempo_inicial = time()
        Autor.objects.all().update(descripcion = 'Descripcion editada con metodo 3')
        tiempo_final = time() - tiempo_inicial
        print(f'Tiempo de Ejecución de método 3: {tiempo_final}')
        """
        tiempo_inicial = time()
        for index,autor in enumerate(autores,10):
            autor.descripcion = f'Descripcion editada con metodo {index}'
        Autor.objects.bulk_update(autores,['descripcion'])
        tiempo_final = time() - tiempo_inicial
        print(f'Tiempo de Ejecución de método 3: {tiempo_final}')
        return render(request,self.template_name)

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


class ListadoLibrosDisponibles(LoginMixin,ListView):
    model = Libro
    paginate_by = 6
    template_name = 'libro/libros_disponibles.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True,cantidad__gte = 1)
        return queryset

class ListadoLibrosReservados(LoginMixin,ListView):
    model = Reserva
    template_name = 'libro/libros_reservados.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True,usuario = self.request.user)
        return queryset

class Reservas(LoginMixin,ListView):
    model = Reserva

    def get_queryset(self):
        return self.model.objects.filter(estado = True,usuario = self.request.user)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('libro:listado_libros_reservados')

class ListadoReservasVencias(LoginMixin,TemplateView):
    template_name = 'libro/reservas_vencidas.html'

class ReservasVencidas(LoginMixin,ListView):
    model = Reserva

    def get_queryset(self):
        return self.model.objects.filter(estado = False,usuario = self.request.user)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('libro:listado_reservas_vencidas')

class DetalleLibroDiponible(LoginMixin,DetailView):
    model = Libro
    template_name = 'libro/detalle_libro_disponible.html'

    def get(self,request,*agrs,**kwargs):
        if self.get_object().cantidad > 0:
            return render(request,self.template_name,{'object':self.get_object()})
        return redirect('libro:listado_libros_disponibles')

class RegistrarReserva(LoginMixin,CreateView):
    model = Reserva
    success_url = reverse_lazy('libro:listado_libros_disponibles')

    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            libro = Libro.objects.filter(id = request.POST.get('libro')).first()
            usuario = Usuario.objects.filter(id = request.POST.get('usuario')).first()
            if libro and usuario:
                if libro.cantidad > 0:
                    nueva_reserva = self.model(
                        libro = libro,
                        usuario = usuario
                    )
                    nueva_reserva.save()
                    mensaje = f'{self.model.__name__} registrada correctamente!'
                    error = 'No hay error!'
                    response = JsonResponse({'mensaje': mensaje, 'error': error,'url':self.success_url})
                    response.status_code = 201
                    return response
        return redirect('libro:listado_libros_disponibles')