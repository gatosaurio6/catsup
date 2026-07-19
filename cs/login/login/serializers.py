from rest_framework import serializers
from .models import Usuario

class RegisterSerializer(serializers.ModelSerializer):
    contraseña = serializers.CharField(write_only=True, source='password')

    class Meta:
        model = Usuario
        fields = ('id', 'correo', 'contraseña', 'username', 'fecha_creacion')
        read_only_fields = ('id', 'fecha_creacion')

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            correo=validated_data['correo'],
            password=validated_data['password'] 
        )
        return user