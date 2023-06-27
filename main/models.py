from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


# Create your models here.

class Staff(models.Model):
    name = models.CharField(max_length=500)
    phone = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    staff_id = models.CharField(unique=True, max_length=999, primary_key=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=999, unique=True, primary_key=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=999, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    credible = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/register-client"


class Order(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        null=True
    )
    staff = models.ManyToManyField(Staff)
    id = models.IntegerField(unique=True, primary_key=True,
                             validators=[MaxValueValidator(999999999), MinValueValidator(100000000)])
    amount = models.IntegerField()
    description = models.CharField(max_length=999)
    sample = models.ImageField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

#    def get_absolute_url(self):
#        return reverse('', args=(str(self.id)))
