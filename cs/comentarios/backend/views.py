from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import comentario
# Create your views here.

def lc (request, id_post):
    cf = comentario.objects.filter(id_post=id_post)
    lista_comentarios = [
        {
            "id": c.id,
            "id_post": c.id_post,
            "id_usuario": c.id_usuario,
            "contenido": c.contenido,
            "fecha_publicacion": c.fecha_publicacion
        }
        for c in cf
    ]
    return JsonResponse({"status": "success", "comments": lista_comentarios}, safe=False)

@csrf_exempt
def cc(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_usuario = data.get("id_usuario")
            contenido = data.get("contenido")
            id_post = data.get("id_post")

            if not id_post:
                return JsonResponse({"status": "error", "message": "El post no existe"}, status=400)
            
            if not contenido:
                return JsonResponse({"status": "error", "message": "El contenido del comentario no puede estar vacio"}, status=400)
            
            nc=comentario.objects.create(
                id_post= int(id_post),
                id_usuario= int(id_usuario),
                contenido= contenido
            )

            return JsonResponse({
                "status": "success", 
                "comment": {
                    "id": nc.id,
                    "id_post": nc.id_post,
                    "id_usuario": nc.id_usuario,
                    "contenido": nc.contenido,
                    "fecha_publicacion": nc.fecha_publicacion
                }
            }, status=201)
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)