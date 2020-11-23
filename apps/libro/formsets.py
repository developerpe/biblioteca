from django.forms import formset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from apps.libro.models import Autor
from apps.libro.forms import AutorForm

class FormsetAutor(FormView):
    template_name = 'libro/autor/autor_formset.html'
    form_class = formset_factory(AutorForm,extra = 1)
    success_url = reverse_lazy('libro:inicio_autor')

    def form_valid(self,form):
        for f in form:
            if f.is_valid():
                f.save()
                #print(f)
        return super().form_valid(form)