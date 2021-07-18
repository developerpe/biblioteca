from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save,pre_save

from apps.usuario.models import Usuario

class Autor(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 200, blank = False, null = False)
    apellidos = models.CharField(max_length = 220, blank = False, null = False)
    nacionalidad = models.CharField(max_length = 100, blank = False, null = False)
    descripcion = models.TextField(blank = False,null = False)
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)       

    all_cruds_types = True

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
    cantidad = models.PositiveIntegerField('Cantidad o Stock',default = 1)
    imagen = models.ImageField('Imagen', upload_to='libros/',max_length=255,null = True,blank = True)
    autor_id = models.ManyToManyField(Autor)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)
    estado = models.BooleanField(default = True, verbose_name = 'Estado')

    def natural_key(self):
        return self.titulo

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo  


    def obtener_autores(self):
        autores = str([autor for autor in self.autor_id.all().values_list('nombre',flat = True)]).replace("[","").replace("]","").replace("'","")
        return autores

class Reserva(models.Model):
    """Model definition for Reserva."""

    # TODO: Define fields here
    id = models.AutoField(primary_key = True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad_dias = models.SmallIntegerField('Cantidad de Dias a Reservar',default = 7)    
    fecha_creacion = models.DateField('Fecha de creación', auto_now = False, auto_now_add = True)
    fecha_vencimiento = models.DateField('Fecha de vencimiento de la reserva', auto_now=False, auto_now_add=False, null = True, blank = True)
    estado = models.BooleanField(default = True, verbose_name = 'Estado')

    class Meta:
        """Meta definition for Reserva."""

        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        """Unicode representation of Reserva."""
        return f'Reserva de Libro {self.libro} por {self.usuario}'

def quitar_relacion_autor_libro(sender,instance,**kwargs):
    if instance.estado == False:
        autor = instance.id
        libros = Libro.objects.filter(autor_id=autor)
        for libro in libros:
            libro.autor_id.remove(autor)

def reducir_cantidad_libro(sender,instance,**kwargs):
    libro = instance.libro
    if libro.cantidad > 0:
        libro.cantidad = libro.cantidad - 1
        libro.save()

def validar_creacion_reserva(sender,instance,**kwargs):
    libro = instance.libro
    if libro.cantidad < 1:
        raise Exception("No puede realizar esta reserva")

def agregar_fecha_vencimiento_reserva(sender,instance,**kwargs):
    if instance.fecha_vencimiento is None or instance.fecha_vencimiento == '':
        instance.fecha_vencimiento = instance.fecha_creacion + timedelta(days = instance.cantidad_dias)
        instance.save()

def saludar(sender,instance,**kwargs):
    print("Hola desde signal de autor")

post_save.connect(quitar_relacion_autor_libro,sender = Autor)
#post_save.connect(saludar,sender = Autor)
post_save.connect(reducir_cantidad_libro,sender = Reserva)
post_save.connect(agregar_fecha_vencimiento_reserva,sender = Reserva)
#pre_save.connect(validar_creacion_reserva,sender = Reserva)