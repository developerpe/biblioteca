from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

class Autor(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 200, blank = False, null = False)
    apellidos = models.CharField(max_length = 220, blank = False, null = False)
    nacionalidad = models.CharField(max_length = 100, blank = False, null = False)
    descripcion = models.TextField(blank = False,null = False)
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)

       

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nombre']

    def natural_key(self):
        return f'{self.nombre} {self.apellidos}'

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    id = models.AutoField(primary_key = True)
    titulo = models.CharField('Título', max_length = 255, blank = False, null = False)
    fecha_publicacion = models.DateField('Fecha de publicación', blank = False, null = False)
    descripcion = models.TextField('Descripción',null = True,blank = True)
    cantidad = models.SmallIntegerField('Cantidad o Stock',default = 1)
    imagen = models.ImageField('Imagen', upload_to='libros/',max_length=255,null = True,blank = True)
    autor_id = models.ManyToManyField(Autor)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)
    estado = models.BooleanField(default = True, verbose_name = 'Estado')

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

def quitar_relacion_autor_libro(sender,instance,**kwargs):
    if instance.estado == False:
        autor = instance.id
        libros = Libro.objects.filter(autor_id=autor)
        for libro in libros:
            libro.autor_id.remove(autor)

post_save.connect(quitar_relacion_autor_libro,sender = Autor)