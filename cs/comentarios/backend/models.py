from django.db import models

# Create your models here.
class comentario(models.Model):
    id = models.AutoField(primary_key=True)
    id_post = models.IntegerField(db_column='id_post')
    id_usuario = models.IntegerField(db_column='id_usuario')
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comentario'
        managed = True

    def __str__(self):
        return f"Comentario {self.id} de usuario {self.id_usuario} en post {self.id_post}"