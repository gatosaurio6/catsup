from django.db import models

# Create your models here.
class Usuario(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    username = models.CharField(max_length=255)

    class Meta:
        db_table = "usuario"
        managed = False

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = "Post"
        managed = False

class comentario(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comentario'
        managed = True

    def __str__(self):
        return f"Comentario {self.id} de usuario {self.id_usuario} en post {self.id_post}"