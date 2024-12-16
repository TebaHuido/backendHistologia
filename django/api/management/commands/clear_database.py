from django.core.management.base import BaseCommand
from api.models import Categoria, Sistema, Organo, Captura, Tincion, Muestra

class Command(BaseCommand):
    help = 'Clear the database of all categories, systems, organs, captures, stains, and samples'

    def handle(self, *args, **kwargs):
        Categoria.objects.all().delete()
        Sistema.objects.all().delete()
        Organo.objects.all().delete()
        Captura.objects.all().delete()
        Tincion.objects.all().delete()
        Muestra.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Database cleared successfully'))
