from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

class Staff(models.Model):
    name = models.CharField(max_length=500)
    phone = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    staff_id = models.CharField(unique=True, max_length=999, primary_key=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=999, unique=True, primary_key=True)
    email = models.EmailField()
    phone = models.CharField(max_length=999)
    credible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT
    )
    staff = models.ManyToManyField(Staff)
    id = models.IntegerField(unique=True, primary_key=True,
                             validators=[MaxValueValidator(999999999), MinValueValidator(100000000)])
    amount = models.IntegerField()
    description = models.CharField(max_length=999)
    sample = models.ImageField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
