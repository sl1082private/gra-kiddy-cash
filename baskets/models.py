from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Basket(models.Model):
  created = models.DateTimeField('date created')
  last_modified = models.DateTimeField('date last modified')
  created_by = models.ForeignKey(User)#, unique=True) 
  is_complete = models.BooleanField(default=False)

  def __str__(self):
    return "basket_{}".format(self.id)

  def save(self, *args, **kwargs):
      if not self.pk:
          # This code only happens if the objects is
          # not in the database yet. Otherwise it would
          # have pk
          self.created = timezone.now()
          self.last_modified = self.created
      else:
          self.last_modified = timezone.now()
      super(Basket, self).save(args, kwargs)


class Item(models.Model):
  basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
  vendorID = models.IntegerField(default=0, help_text="reference to vendor")
  price = models.FloatField(default=0.0, help_text="price in EUR")
  created_by = models.ForeignKey(User)#, unique=True)
  created = models.DateTimeField('date created')

  def __str__(self):
    return "{:.2f} EUR (vendor: {}; basket: {})".format(self.price, self.vendorID, self.basket.id)

  def save(self, *args, **kwargs):
      if not self.pk:
          # This code only happens if the objects is
          # not in the database yet. Otherwise it would
          # have pk
          self.created = timezone.now()
      super(Item, self).save(args, kwargs)


