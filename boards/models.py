from django.db import models

class Moodboard(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    background_color=models.CharField(max_length=20, default="#ffffff")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title