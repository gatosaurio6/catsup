from rest_framework import serializers
from .models import comentario

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = comentario
        fields = '__all__'
        read_only_fields = ('id', 'fecha_publicacion') # nose puede modifica si no ere bakan