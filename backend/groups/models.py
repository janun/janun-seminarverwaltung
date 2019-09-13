from django.db import models
from django.utils.text import slugify
from django.db.models import Count, Sum


class JANUNGroupQuerySet(models.QuerySet):
    def add_annotations(self):
        return self.annotate(
            seminar_count=Count("seminars"),
            actual_tnt_sum=Sum("seminars__actual_attendence_days_total"),
        )


class JANUNGroupManager(models.Manager.from_queryset(JANUNGroupQuerySet)):
    def get_queryset(self):
        return super().get_queryset().add_annotations()


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

    objects = JANUNGroupManager()

    class Meta:
        ordering = ("name",)
        verbose_name = "JANUN-Gruppe"
        verbose_name_plural = "JANUN-Gruppen"
