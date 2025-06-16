from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(unique=True, max_length=50)
    code = models.CharField(unique=True, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'