from django.db import models

# Create your models here.

class ranking (models.Model):
    id = models.AutoField(primary_key=True)
    id_post = models.IntegerField(db_column="id_post", null=True, blank=True)
    id_comentario = models.IntegerField(db_column="id_comentario", null=True, blank=True)
    id_usuario = models.IntegerField(db_column="id_usuario")
    OPCIONES_VALOR = [(-1, "dislike"), (1,"like"),]
    valor = models.IntegerField(choices=OPCIONES_VALOR)

    class Meta:
        db_table = "ranking"
        managed = True