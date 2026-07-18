from django.db import models

class CatProfile(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    cat = models.ForeignKey(CatProfile, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='cats_photos/', null=True, blank=True) 
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post de {self.cat.name} - {self.created_at}"

#comentarios 
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50, default="LoverCat")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.author} en Post #{self.post.id}"