from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Event(models.Model):
  event_name = models.CharField('name of event', max_length=127)
  event_date = models.DateField('date of event')
  description = models.TextField('description of event')
  created_by = models.ForeignKey(User)
  created = models.DateTimeField('date created')

  def __str__(self):
#    return "Event '{}' ({})".format(self.event_name, self.event_date)
    return "{}".format(self.event_name)

  def save(self, *args, **kwargs):
      if not self.pk:
          # This code only happens if the objects is
          # not in the database yet. Otherwise it would
          # have pk
          self.created = timezone.now()
      super(Event, self).save(args, kwargs)



class Basket(models.Model):
  created = models.DateTimeField('date created')
  last_modified = models.DateTimeField('date last modified')
  created_by = models.ForeignKey(User)#, unique=True) 
  is_complete = models.BooleanField(default=False)
  event = models.ForeignKey(Event, default=1)

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
  event = models.ForeignKey(Event, default=1)

  def __str__(self):
    return "ID{}: {:.2f} EUR (vendor: {}; basket: {})".format(self.pk, self.price, self.vendorID, self.basket.id)

  def save(self, *args, **kwargs):
      if not self.pk:
          # This code only happens if the objects is
          # not in the database yet. Otherwise it would
          # have pk
          self.created = timezone.now()
          self.basket.save()
      super(Item, self).save(args, kwargs)



class CurrentEvent(models.Model):
  event_id = models.ForeignKey(Event)
  ## in case more than one entry exists, use most recent one
  last_touched = models.DateTimeField('date last touched')

  def __str__(self):
#    return "Current event_id: {} ({})".format(self.event_id, self.last_touched)
    return "{}".format(self.event_id)
