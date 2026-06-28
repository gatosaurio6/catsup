from rest_framework import serializers
from .models import CatRanking

class CatRankingSerializer(serializers.ModelSerializer):
    nombre_del_gato = serializers.StringRelatedField(source='gato')

    class Meta:
        model = CatRanking
        fields = ['id', 'gato', 'nombre_del_gato', 'puntos']