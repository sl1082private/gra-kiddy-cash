from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

import collections

from .models import Basket, Item, Event, CurrentEvent

# Create your views here.

@login_required
def redirect_index(request):
  return HttpResponseRedirect('baskets')

@login_required
def vendors_old(request):
  vendor_dict = dict()
  #item_list = Item.objects.all()
  item_list = Item.objects.filter(event=get_current_event())
  for item in item_list:
    if not item.vendorID in vendor_dict:
      vendor_dict[item.vendorID] = [1, item.price]
    else:
      vendor_dict[item.vendorID][0] += 1
      vendor_dict[item.vendorID][1] += item.price

  vo = collections.OrderedDict(sorted(vendor_dict.items()))
  context = {
      'vendor_dict': vo,
  }
  return render(request, 'baskets/vendors.html', context)


@login_required
def vendors(request):
  vendor_dict = dict()
  baskets_list = Basket.objects.filter(event=get_current_event())
  item_list = Item.objects.all()
  #item_list = Item.objects.filter(event=get_current_event())
  for item in item_list:
    if not item.basket in baskets_list:
    # only consider items in baskets that belong to the current event
      continue
    if not item.vendorID in vendor_dict:
      vendor_dict[item.vendorID] = [1, item.price]
    else:
      vendor_dict[item.vendorID][0] += 1
      vendor_dict[item.vendorID][1] += item.price

  vo = collections.OrderedDict(sorted(vendor_dict.items()))
  context = {
      'vendor_dict': vo,
  }
  return render(request, 'baskets/vendors.html', context)



@login_required
def baskets(request):
  current_event = get_current_event()
  basket_list = Basket.objects.filter(event=current_event).order_by('-last_modified')
  context = {
      'basket_list': basket_list,
      'current_event': current_event.event_name,
      }
  return render(request, 'baskets/index.html', context)
## two lines below achieve the same as 'render':
#  template = loader.get_template('baskets/index.html')
#  return HttpResponse(template.render(context, request))


@login_required
def detail(request, basket_id):
#  heading = "Content of <b>basket %s</b>:<br><p>\n" % basket_id
#  item_list = Item.objects.filter(basket=basket_id)
#  html = heading + '<br>\n'.join([i.__str__() for i in item_list])
#  return HttpResponse(html)
### The following fails, if there are no items assigned to a basket. We do
### not want this behavior.
#  item_list = get_list_or_404(Item, basket=basket_id)
  item_list = Item.objects.filter(basket=basket_id)
  basket_sum = Item.objects.filter(basket=basket_id).aggregate(Sum('price'))
  context = {
      'basket_id': basket_id,
      'item_list': item_list,
      'basket_sum': basket_sum['price__sum'],
      }
  return render(request, 'baskets/detail.html', context)

@login_required
def delete_item(request, basket_id, item_id):
  item = get_object_or_404(Item, pk=item_id)
  print ( "remove item pk={}".format(item_id) )
  item.delete()
  return HttpResponseRedirect(reverse('detail', args=(basket_id,)))

def get_current_event():
  current_event = CurrentEvent.objects.latest('last_touched')
  #event = get_object_or_404(Event, pk=current_event.event_id)
  return current_event.event_id
  #return event

@login_required
def add_item(request, basket_id):
  basket = get_object_or_404(Basket, pk=basket_id)
  item = Item(basket=basket, vendorID=request.POST['vendorID'],
      price=request.POST['price'],created_by=request.user,
      event=get_current_event())
  item.save()
  return HttpResponseRedirect(reverse('detail', args=(basket.id,)))


@login_required
def add_basket(request):
  basket = Basket(created_by=request.user, event=get_current_event())
  basket.save()
  return HttpResponseRedirect(reverse('detail', args=(basket.id,)))
