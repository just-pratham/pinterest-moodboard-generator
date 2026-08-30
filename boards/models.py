from django.db import models
from django.db.models import Q

class Moodboard(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    background_color = models.CharField(max_length=20, default="#ffffff")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MoodboardImage(models.Model):
    moodboard = models.ForeignKey(
        Moodboard,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image_url = models.URLField()

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    unsplash_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['moodboard', 'unsplash_id'],
                condition=Q(unsplash_id__isnull=False),
                name='unique_unsplash_image_per_moodboard'
            )
        ]

    def __str__(self):
        return self.caption or f"Image for {self.moodboard.title}"