from django.db import models
from accounts.models import Profile


class Car(models.Model):
    USED = 'used'
    UNUSED = 'unused'
    CONDITION = (
        ('used', 'It is used'),
        ('unused', 'It is not used')
    )
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    body_style = models.CharField(max_length=100, null=True, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    engine = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    transmission = models.CharField(max_length=100, null=True, blank=True)
    interior = models.CharField(max_length=100, null=True, blank=True)
    conditon = models.CharField(max_length=100, choices=CONDITION, default=UNUSED)
    fuel_type = models.CharField(max_length=100, null=True, blank=True)
    owner = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
# class SendMessage(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     sender = models.

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    number = models.IntegerField()
    message = models.TextField()

    def __str__(self) -> str:
        return self.full_name
    
class CarMessage(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"