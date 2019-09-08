from django.db import models
from django.utils.text import slugify


class JANUNGroup(models.Model):
    slug = models.SlugField(unique=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "JANUN-Gruppe"
        verbose_name_plural = "JANUN-Gruppen"
