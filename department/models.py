from django.db import models


class Department(models.Model):
    name = models.CharField(unique=True, max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    department_head = models.ManyToManyField('user.AuthUser', related_name="department_head")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'