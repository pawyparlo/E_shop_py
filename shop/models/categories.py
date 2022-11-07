from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to="categories/%Y/%m%d", blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

