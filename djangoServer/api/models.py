import uuid
import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{extension}"
    return os.path.join('muestras/', new_filename)

class Muestra(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    image = models.ImageField(upload_to=generate_filename, null=False, blank=False, verbose_name="Imagen")
    
    def __str__(self):
        return f"Muestra {self.id}: {self.name}"

    class Meta:
        verbose_name = "Muestra"
        verbose_name_plural = "Muestras"

    def get_filename(self):
        return os.path.basename(self.image.name)

@receiver(pre_delete, sender=Muestra)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
                print(f"Imagen {image_path} eliminada con éxito.")
            except Exception as e:
                print(f"Error al eliminar la imagen {image_path}: {e}")
