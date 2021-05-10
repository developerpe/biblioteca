DOCUMENTACIÓN DE BIBLIOTECA
===========================

Esta es una documentación de prueba creada dentro del Curso de Django
utilizando la librería MKDOCS para publicarlo en **ReadTheDocs**

Requerimientos
--------------

-  Clona el siguiente repositorio: `Repositorio de
   Biblioteca <https://github.com/developerpe/biblioteca>`__.

Login
-----

.. code:: python

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

Project layout
--------------

::

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

