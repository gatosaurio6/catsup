from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from .models import Post
from django.shortcuts import get_object_or_404
#import os
#from azure.storage.blob import BlobServiceClient
# Create your views here.

class gp (APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        archivo = request.FILES.get("archivo")
        id_usuario = request.user
        titulo = request.data.get ("titulo")
        url_multimedia = request.data.get("url_multimedia")
        tipo = request.data.get("tipo")
        formato = request.data.get("formato")

        if archivo:
            nombre_archivo = archivo.name
            formato = nombre_archivo.split('.')[-1].lower()
            tipo = "image" if formato in Post.FORMATOS_IMAGE else "video"
#            conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#            if conn_str:
#                try:
#                    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
#                    blob_client = blob_service_client.get_blob_client(container="multimedia", blob=nombre_archivo)
#                    blob_client.upload_blob(archivo, overwrite=True)
#                    url_multimedia = blob_client.url
#                except Exception as e:
#                    return Response({"error": f"fallo al subir a Azure: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        nuevo_post = Post(
            id_usuario=request.user,
            titulo=titulo,
            url_multimedia=url_multimedia,
            tipo=tipo,
            formato=formato
        )

        try:
            nuevo_post.save()
            return Response({
                "id": nuevo_post.id,
                "id_usuario": nuevo_post.id_usuario,
                "titulo": nuevo_post.titulo,
                "url_multimedia": nuevo_post.url_multimedia,
                "tipo": nuevo_post.tipo,
                "formato": nuevo_post.formato,
                "fecha_publicacion": nuevo_post.fecha_publicacion
            }, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        posts = Post.objects.all().order_by("-fecha_publicacion")
        lista_post =[
            {
                "id": p.id,
                "titulo": p.titulo,
                "url_multimedia": p.url_multimedia,
                "fecha": p.fecha_publicacion.strftime("%Y-%m-%d %H:%M"),
                "autor": p.id_usuario.username
            } for p in posts
        ]
        return Response(lista_post, status=status.HTTP_200_OK)
        
class ep (APIView):
    permission_classes = [IsAuthenticated]
    
    def delete (self,request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        if post.id_usuario.id != request.user.id:
            return Response({"error": "Acceso no permitido"}, status=status.HTTP_403_FORBIDDEN)
        
        if post.url_multimedia:
#            conn_str = os.gatenv("AZURE_STORAGE_CONNECTIONSTRING")
#
#            if not conn_str:
#                return Response({"error": "Error al obtener acceso"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#            
#            try:
#                blob_service_client = BlobServiceClient.from_connection_string(conn_str)
#                nombre_archivo = post.url_multimedia.split("/")[-1]
#
#                if nombre_archivo:
#                    blob_client= blob_service_client.get_blob_client(container="multimedia", blob=nombre_archivo)
#                    blob_client.delete_blob()
#            except ResourceNotFoundError:
#                pass
#            except Exception as e:
#                return Response({"error": f"Fallo de storage: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            pass
        post.delete()
        return Response({"mensaje": "Post eliminado"}, status=status.HTTP_200_OK)
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        datos_post = {
            "id": post.id,
            "id_usuario": post.id_usuario.id,
            "titulo": post.titulo,
            "url_multimedia": post.url_multimedia,
            "fecha_publicacion": post.fecha_publicacion
        }
        return Response (datos_post, status=status.HTTP_200_OK)