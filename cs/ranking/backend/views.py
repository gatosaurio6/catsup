from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import ranking
from rest_framework.permissions import IsAuthenticated

class rv(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        id_usuario = request.user.id
        id_post = request.data.get("id_post")
        id_comentario = request.data.get("id_comentario")
        accion = request.data.get("accion")

        if accion == "like":
            valor_voto = 1
        elif accion == "dislike":
            valor_voto = -1
        else:
            return Response ({"error": "Accion invalida"}, status=status.HTTP_400_BAD_REQUEST)
        
        voto_existente = ranking.objects.filter(
            id_usuario = id_usuario,
            id_post = id_post,
            id_comentario = id_comentario,
        ).first()

        if voto_existente:
            if voto_existente.valor == valor_voto:
                voto_existente.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                voto_existente.valor = valor_voto
                voto_existente.save()
                return Response(status=status.HTTP_200_OK)
        
        ranking.objects.create(
            id_usuario = id_usuario,
            id_post = id_post,
            id_comentario = id_comentario,
            valor = valor_voto
        )
        return Response(status=status.HTTP_201_CREATED)
    
class total(APIView):
    def post(self, request):
        id_posts = request.data.get("id_posts", [])
        if not id_posts:
            return Response([], status=status.HTTP_200_OK)
        
        resultados = (
            ranking.objects.filter(id_post__in=id_posts)
            .values("id_post")
            .annotate(total_puntos=Sum("valor"))
        )

        puntos_mapeados = {item["id_post"]: item["total_puntos"] for item in resultados}

        respuesta_final = {
            id_post: puntos_mapeados.get(id_post,0)
            for id_post in id_posts
        }

        return Response(respuesta_final, status=status.HTTP_200_OK)