from django.db import models

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=50)
    main = models.TextField()
    seasoning = models.TextField(blank=True)
    oils = models.TextField(blank=True)
    preparation = models.TextField(default="Yummy")
