from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, username, correo, password=None):
        if not correo:
            raise ValueError('El usuario debe tener un correo')
        user = self.model(
            username=username, 
            correo=self.normalize_email(correo)
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True, db_column='ID')
    correo = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo']

    class Meta:
        db_table = 'usuario'
        managed = True