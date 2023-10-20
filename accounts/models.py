from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username
    
    @property
    def age(self):
        today = date.today()
        birth_date = self.birth_date
        age = today.year - birth_date.year - ((today.month, today.today) < (birth_date.month, birth_date.today))
        return age