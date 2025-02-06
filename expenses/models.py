from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from decimal import Decimal

# Create your models here.
class Expense(models.Model):
    customer_name = models.CharField(max_length=100)
    category = models.CharField(max_length=266)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    amount = models.FloatField()
    date = models.DateField(default=now)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)


def save(self, *args, **kwargs):
    self.total_price = Decimal(self.quantity) * Decimal(str(self.amount))
    super().save(*args, **kwargs)


    def __str__(self):
        return self.category
    def __str__(self):
        return self.product_name

    class Meta:
        ordering= ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class product_name(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'product_names'

    def __str__(self):
        return self.name