from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.

class Usuario(models.Model):
    id = models.AutoField(primary_key= True, db_column="ID")
    username = models.CharField(max_length=255)

    class Meta:
        db_table = "usuario"
        managed = False

class Post (models.Model):
    FORMATOS_IMAGE = ["jpg", "jpeg", "webp", "png", "gif"]
    FORMATOS_VIDEO = ["mp4", "avi", "webm"]
    TIPO_CHOICES = [("image", "Image"), ("video", "Video"),]
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,)
    titulo = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    url_multimedia = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=5, choices = TIPO_CHOICES, null=True, blank=True)
    formato = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        db_table = "publicacion"
        managed = True

    def clean(self):
        super().clean()
        error = "não não amigão"
        if self.formato:
            self.formato = self.formato.lower()
        if self.tipo == "image":
            if self.formato not in self.FORMATOS_IMAGE:
                raise ValidationError({"formato": error })
        if self.tipo == "video":
            if self.formato not in self.FORMATOS_VIDEO:
                raise ValidationError({"formato": error})
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def url_completa(self):
        if self.url_multimedia:
            return f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_CONTAINER}/{self.url_multimedia}"
        return None

    def __str__(self):
        return f"post {self.id}: {self.titulo} [{self.tipo}/{self.formato}]"