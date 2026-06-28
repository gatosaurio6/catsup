from django.db import models
from gallery.models import CatProfile 

class CatRanking(models.Model):
    gato = models.OneToOneField(CatProfile, on_delete=models.CASCADE, related_name='ranking')
    puntos = models.IntegerField(default=0)
    
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Puntaje de {self.gato} - {self.puntos} pts"
    
    #cuando esté listo el terrafrom usar el "python manage.py makemigrations ranking_app" y luego 
    #"python manage.py migrate" 