from django.db import models

class CatProfile(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    cat = models.ForeignKey(CatProfile, on_delete=models.CASCADE, related_name='posts')
    image_url = models.URLField() # Por ahora usaremos URL, después lo cambiamos a archivo físico para la nube
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post de {self.cat.name} - {self.created_at}"