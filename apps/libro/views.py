from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.urls import reverse_lazy
from .forms import AutorForm,LibroForm
from .models import Autor,Libro

class Inicio(TemplateView):
    template_name = 'index.html'


class ListadoAutor(ListView):
    model = Autor
    template_name = 'libro/autor/listar_autor.html'
    context_object_name = 'autores'
    queryset = Autor.objects.filter(estado = True)


class ActualizarAutor(UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/crear_autor.html'
    success_url = reverse_lazy('libro:listar_autor')

class CrearAutor(CreateView):
    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/crear_autor.html'
    success_url = reverse_lazy('libro:listar_autor')

class EliminarAutor(DeleteView):
    model = Autor

    def post(self,request,pk,*args,**kwargs):
        object = Autor.objects.get(id = pk)
        object.estado = False
        object.save()
        return redirect('libro:listar_autor')

class ListadoLibros(ListView):
    model = Libro
    template_name = 'libro/libro/listar_libro.html' # queryset = Libro.objects.all()
    queryset = Libro.objects.filter(estado = True)

class CrearLibro(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/crear_libro.html'
    success_url = reverse_lazy('libro:listado_libros')

class ActualizarLibro(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/crear_libro.html'
    success_url = reverse_lazy('libro:listado_libros')

class EliminarLibro(DeleteView):
    model = Libro

    def post(self,request,pk,*args,**kwargs):
        object = Libro.objects.get(id = pk)
        object.estado = False
        object.save()
        return redirect('libro:listado_libros')
