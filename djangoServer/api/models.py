import uuid
import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{extension}"
    return os.path.join('imagens/', new_filename)

class Profesor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    passhash = models.CharField(max_length=100, verbose_name="Hash")
    correo = models.CharField(max_length=100, verbose_name="Correo")

    def __str__(self):
        return f"Profesor: {self.nombre} ({self.correo})"
   
class Curso(models.Model):
    asignatura = models.CharField(max_length=100, verbose_name="Asignatura")
    anio = models.IntegerField()
    semestre = models.BooleanField()
    grupo = models.CharField(max_length=1, verbose_name="Grupo")
    profesor = models.ForeignKey(Profesor, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Curso: {self.asignatura} ({self.anio} - {'S1' if self.semestre else 'S2'})"
    
class Ayudante(models.Model):
    niveldeacceso = models.CharField(max_length=5, verbose_name="Nivel de acceso")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    passhash = models.CharField(max_length=100, verbose_name="Hash")
    correo = models.CharField(max_length=100, verbose_name="Correo")
    curso = models.ManyToManyField(Curso)

    def __str__(self):
        return f"Ayudante: {self.nombre} ({self.correo})"
 
class Categoria(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return f"Categoría: {self.name}"
    
class Sistema(models.Model):
    sisname = models.CharField(max_length=100, verbose_name="Nombre del sistema")

    def __str__(self):
        return f"Sistema: {self.sisname}"
    
class Organo(models.Model):
    orgname = models.CharField(max_length=100, verbose_name="Nombre del organo")
    sistema = models.ManyToManyField(Sistema)

    def __str__(self):
        return f"Órgano: {self.orgname}"
    
class Muestra(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    Categoria = models.ManyToManyField(Categoria)
    curso = models.ManyToManyField(Curso, through='Lote')
    organo = models.ManyToManyField(Organo)

    def __str__(self):
        return f"Muestra: {self.name}"

class Lote(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    curso = models.ForeignKey(Curso, models.SET_NULL, null=True, blank=True)
    muestra = models.ForeignKey(Muestra, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Lote: {self.name}"
    
class Alumno(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    passhash = models.CharField(max_length=100, verbose_name="Hash")
    correo = models.CharField(max_length=100, verbose_name="Correo")
    curso = models.ManyToManyField(Curso)
    permiso = models.ManyToManyField(Muestra)

    def __str__(self):
        return f"Alumno: {self.nombre} ({self.correo})"
    
class Captura(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    image = models.ImageField(upload_to=generate_filename, null=False, blank=False, verbose_name="Imagen")
    muestra = models.ForeignKey(Muestra, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Imagen {self.id}: {self.name}"

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"

    def get_filename(self):
        return os.path.basename(self.image.name)

@receiver(pre_delete, sender=Captura)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
                print(f"Imagen {image_path} eliminada con éxito.")
            except Exception as e:
                print(f"Error al eliminar la imagen {image_path}: {e}")
