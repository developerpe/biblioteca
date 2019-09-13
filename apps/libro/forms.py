from django import forms
from .models import Autor,Libro

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre','apellidos','nacionalidad','descripcion']
        labels = {
            'nombre': 'Nombre del autor',
            'apellidos': 'Apellidos del autor',
            'nacionalidad': 'Nacionalidad del autor',
            'descripcion': 'Pequeña descripción',
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre del autor',
                    'id': 'nombre'
                }
            ),
            'apellidos': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese los apellidos del autor',
                    'id':'apellidos'
                }
            ),
            'nacionalidad':forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese una nacionalidad para el autor',
                    'id':'nacionalidad'
                }
            ),
            'descripcion': forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Ingrese una pequeña descripcion para el autor',
                    'id':'descripcion'
                }
            )
        }

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('titulo','autor_id','fecha_publicacion')
        label = {
            'titulo':'Título del libro',
            'autor_id': 'Autor(es) del Libro',
            'fecha_publicacion': 'Fecha de Publciación del Libro'
        }
        widgets = {
            'titulo': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese título de libro'
                }
            ),
            'autor_id': forms.SelectMultiple(
                attrs = {
                    'class':'form-control'
                }
            ),
            'fecha_publicacion': forms.SelectDateWidget(
                attrs = {
                    'class': 'form-control'
                }
            )
        }
