from rest_framework import serializers
from .models import comentario

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = comentario
        fields = '__all__' 
        # niuno puede modificar los id fecha y eso
        read_only_fields = ('id', 'fecha_publicacion', 'id_usuario')