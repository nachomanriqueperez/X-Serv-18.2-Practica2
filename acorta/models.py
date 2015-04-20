from django.db import models

# Create your models here.
class url_Acortar(models.Model):
    Url = models.CharField(max_length=300)
