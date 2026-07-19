from django.db import models
from django.core.exceptions import ValidationError

class ranking(models.Model):
    id = models.AutoField(primary_key=True)
    id_post = models.IntegerField(db_column="id_post", null=True, blank=True)
    id_comentario = models.IntegerField(db_column="id_comentario", null=True, blank=True)
    id_usuario = models.IntegerField(db_column="id_usuario")
    OPCIONES_VALOR = [(-1, "dislike"), (1, "like")]
    valor = models.IntegerField(choices=OPCIONES_VALOR)

    class Meta:
        db_table = "ranking"
        managed = True

    def clean(self):
        super().clean()
        error = "não não amigão"

        valores_permitidos = [opcion[0] for opcion in self.OPCIONES_VALOR]
        if self.valor not in valores_permitidos:
            raise ValidationError({"valor": error})
        
        if not self.id_post and not self.id_comentario:
            raise ValidationError(error)
        if self.id_post and self.id_comentario:
            raise ValidationError(error)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)