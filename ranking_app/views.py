from rest_framework import generics
from .models import CatRanking
from .serializers import CatRankingSerializer

class TopCatsListView(generics.ListAPIView):
    # El signo menos (-) antes de "puntos" es vital: le dice a Django 
    # que ordene de Mayor a Menor (Descendente). 
    # El [:10] al final asegura que solo enviemos el Top 10.
    queryset = CatRanking.objects.all().order_by('-puntos')[:10]
    serializer_class = CatRankingSerializer