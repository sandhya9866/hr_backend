from django.db import models
from user.models import AuthUser

# Create your models here.
class Shift(models.Model):
    title = models.CharField(max_length=100)
    colour = models.CharField(max_length=20, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    min_start_time = models.TimeField(null=True, blank=True)
    max_end_time = models.TimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
