from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from .models import Basket, Item

# Create your views here.


@login_required
def baskets(request):
  basket_list = Basket.objects.order_by('last_modified')
  context = {
      'basket_list': basket_list,
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



@login_required
def add_item(request, basket_id):
  basket = get_object_or_404(Basket, pk=basket_id)
  item = Item(basket=basket, vendorID=request.POST['vendorID'],
      price=request.POST['price'],created_by=request.user)
  item.save()
  return HttpResponseRedirect(reverse('detail', args=(basket.id,)))


@login_required
def add_basket(request):
  basket = Basket(created_by=request.user)
  basket.save()
  return HttpResponseRedirect(reverse('detail', args=(basket.id,)))
