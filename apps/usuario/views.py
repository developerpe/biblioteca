import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,TemplateView
from apps.usuario.models import Usuario
from apps.usuario.forms import (
    FormularioLogin, FormularioUsuario, CambiarPasswordForm
)
from apps.usuario.mixins import (
    LoginYSuperStaffMixin, ValidarPermisosMixin, LoginMixin
)

from apps.libro.models import Libro,Reserva

class Inicio(LoginRequiredMixin,TemplateView):
    """Clase que renderiza el index del sistema"""

    template_name = 'index.html'
    groups_required = ['Grupo1','Grupo2']

    def get(self,request,*args,**kwargs):
        # SELECT RELATED
        """
        print(Reserva.objects.select_related().all().query)
        reservas = Reserva.objects.select_related().all()
        for reserva in reservas:
            print(reserva.usuario.username)
            print(reserva.libro.titulo)
            print(reserva.libro.fecha_publicacion)
        """

        # PREFETCH RELATED

        print(Libro.objects.prefetch_related('autor_id').all().query)
        print("----------------------------")
        libros = Libro.objects.prefetch_related('autor_id').all()
        for libro in libros:
            print(libro.autor_id.all().query)
            for autor in libro.autor_id.all():                
                print(autor.nombre)
        print("----------------------------")
        """
        contador = 0
        grupos_usuario = request.user.groups.all().values('name')
        for grupo in grupos_usuario:
            if grupo['name'] in self.groups_required:
                contador += 1

        if contador == len(self.groups_required):
            return render(request,self.template_name)
        else:
            print("NO ESTA DENTRO DE LOS GRUPOS")
        # agregar un permiso
        # usuario.user_permissions.add(permiso1,permiso2,...)
        # usuario.user_permissions.remove(permiso1,permiso2,...)
        # usuario.user_permissions.set([lista_permisos])
        # usuario.user_permissions.clear()
        """
        return render(request,self.template_name)

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


class InicioUsuarios(LoginYSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    template_name='usuarios/listar_usuario.html'
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario',
                           'usuario.delete_usuario', 'usuario.change_usuario')


class ListadoUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, ListView):
    model = Usuario
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario',
                           'usuario.delete_usuario', 'usuario.change_usuario')

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)
    
    def get(self,request,*args,**kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('usuarios:inicio_usuarios')


class RegistrarUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'usuarios/crear_usuario.html'
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario',
                           'usuario.delete_usuario', 'usuario.change_usuario')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('usuarios:inicio_usuarios')


class EditarUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'usuarios/editar_usuario.html'
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario',
                           'usuario.delete_usuario', 'usuario.change_usuario')

    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST,instance = self.get_object())
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
            return redirect('usuarios:inicio_usuarios')


class EliminarUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/eliminar_usuario.html'
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario',
                           'usuario.delete_usuario', 'usuario.change_usuario')

    def delete(self,request,*args,**kwargs):
        if request.is_ajax():
            usuario = self.get_object()
            usuario.usuario_activo = False
            usuario.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('usuarios:inicio_usuarios')


class CambiarPassword(LoginMixin, View):
    template_name = 'usuarios/cambiar_password.html'
    form_class = CambiarPasswordForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = Usuario.objects.filter(id=request.user.id)
            if user.exists():
                user = user.first()
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                logout(request)
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form': form})

            