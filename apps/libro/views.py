from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.urls import reverse_lazy
from apps.libro.models import Autor, Libro
from apps.libro.forms import AutorForm,LibroForm


class ListadoAutor(View):
    """Contiene la lógica para el listado de autores.


    :parámetro model: Modelo a utilizarse
    :type model: Model
    :parámetro form_class: Form de Django referente a model
    :type form_class: DjangoForm
    :parámetro template_name: Template a utilizarse en la clase
    :type template_name: str

    """


    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/listar_autor.html'

    def get_queryset(self):
        """Retorna una consulta a utilizarse en la clase.
        Esta funcion se encuentra en toda vista basada en  clase, se utiliza internamente por django para
        generar las consultas de a cuerdo a los valores que se definen en la clase, valores como MODEL,FORM_CLASS


        :return: una consulta
        :rtype: Queryset
        """

        
        return self.model.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        """Retorna un contexto a enviar a template.
        Aquí definimos todas las variables que necesitamos enviar a nuestro template definido en TEMPLATE_NAME,
        se agregan a un diccionario general para poder ser enviados en la funcion RENDER.


        :return: un contexto
        :rtype: dict
        """


        contexto = {}
        contexto['autores'] = self.get_queryset()   #agregamos la consulta al contexto
        contexto['form'] = self.form_class
        return contexto

    def get(self, request, *args, **kwargs):
        """Renderiza un template con un contexto dado.
        Se encarga de manejar toda petición enviada del navegador a Django a través del método GET
        del protocolo HTTP, en este caso renderiza un template definido en TEMPLATE_NAME junto con
        el contexto definido en GET_CONTEXT_DATA.


        :return: render
        :rtype: func
        """


        return render(request, self.template_name, self.get_context_data())

class ActualizarAutor(UpdateView):
    """Contiene la lógica para edición de un Autor


    :parámetro model: Modelo a utilizarse
    :type model: Model
    :parámetro form_class: Form de Django referente a model
    :type form_class: DjangoForm
    :parámetro template_name: Template a utilizarse en la clase
    :type template_name: str
    :parámetro success_url: Url de redireccionado al actualizar
    :type success_url: URL

    """


    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/autor.html'
    success_url = reverse_lazy('libro:listar_autor')

class CrearAutor(CreateView):
    """Contiene la lógica para crear un Autor


    :parámetro model: Modelo a utilizarse
    :type model: Model
    :parámetro form_class: Form de Django referente a model
    :type form_class: DjangoForm
    :parámetro template_name: Template a utilizarse en la clase
    :type template_name: str
    :parámetro success_url: Url de redireccionado al actualizar
    :type success_url: URL

    """


    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/crear_autor.html'
    success_url = reverse_lazy('libro:listar_autor')

class EliminarAutor(DeleteView):
    """Contiene la lógica para eliminar un Autor


    :parámetro model: Modelo a utilizarse
    :type model: Model

    """


    model = Autor

    def post(self,request,pk,*args,**kwargs):
        """Elimina logicamente un objeto.
        Se encarga de manejar las peticiones de tipo POST enviadas del navegador a Django.


        :parámetro pk: clave primaria
        :type pk: int
        :parámetro request: petición enviada del navegador
        :type request: request
        :return: redirect
        :rtype: func
        """


        object = Autor.objects.get(id = pk)
        object.estado = False
        object.save()
        return redirect('libro:listar_autor')



class CrearLibro(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/crear_libro.html'
    success_url = reverse_lazy('libro:listado_libros')

class ListadoLibros(View):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/listar_libro.html'

    def get_queryset(self):
        return self.model.objects.filter(estado = True)

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['libros'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())


class ActualizarLibro(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/libro.html'
    success_url = reverse_lazy('libro:listado_libros')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['libros'] = Libro.objects.filter(estado = True)
        return context

class EliminarLibro(DeleteView):
    model = Libro

    def post(self,request,pk,*args,**kwargs):
        object = Libro.objects.get(id = pk)
        object.estado = False
        object.save()
        return redirect('libro:listado_libros')
