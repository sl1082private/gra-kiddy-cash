from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Sum, Count,F,Q
from django.contrib.auth.decorators import login_required

from io import BytesIO
#from reportlab.pdfgen import canvas

import collections

from .models import Basket, Item, Event, CurrentEvent, Vendor

from .forms import AddItemForm, VendorForm


@login_required
def redirect_index(request):
  return HttpResponseRedirect('baskets')


@login_required
def vendors(request, show_all=False):
  current_event = get_current_event()
  ceid = current_event.id
  #print ("current_event (id={}): {}".format(ceid, current_event))
  #test_q = Item.objects.filter(basket__event__in=(current_event,))
  #print ("test query of items in {}: {}".format(current_event, test_q))
  vendors = Vendor.objects.filter(events__in=(current_event,))
  #sales = Sum('item__price', filter=Q(item__basket__event__in=(current_event,)) )
  #sales = Sum('item__price', filter=Q(item__basket__event__id=ceid) )
  sales = Sum('item__price', filter=Q(item__basket__event=current_event) )
  #num_sales = Count('item', filter=Q(item__basket__event__in=(current_event,)) )
  num_sales = Count('item', filter=Q(item__basket__event=current_event) )
  sales_net = F('sales')*0.88
  sales_12p = F('sales')*0.12
  #print (str( vendors.annotate(sales=sales).annotate(num_sales=num_sales).query ) )
  vendors = vendors.annotate(sales=sales).annotate(num_sales=num_sales)
  vendors = vendors.annotate(sales_net=sales_net).annotate(sales_12p=sales_12p)
  vtotal = vendors.aggregate(sales_sum=Sum('sales'))
  if vtotal['sales_sum']:
    vtotal['sales_sum_net']=vtotal['sales_sum']*0.88
    vtotal['sales_sum_12p']=vtotal['sales_sum']*0.12
  else:
    vtotal = {}

  context = {
      'show_all': show_all,
      'vendors': vendors,
      'vtotal': vtotal, #[vtotal,0.88*vtotal,0.12*vtotal],
      'current_event': current_event.event_name,
      'current_user': request.user,
  }
  return render(request, 'baskets/vendors_new.html', context)




@login_required
def baskets(request):
  current_event = get_current_event()
  current_user = request.user
  basket_list = Basket.objects.filter(event=current_event).order_by('-last_modified')
  context = {
      'basket_list': basket_list,
      'current_event': current_event.event_name,
      'current_user': current_user,
      }
  return render(request, 'baskets/index.html', context)
## two lines below achieve the same as 'render':
#  template = loader.get_template('baskets/index.html')
#  return HttpResponse(template.render(context, request))


@login_required
def vendor_detail(request, vendor_number):
  vendor = Vendor.objects.get(vendor_number=vendor_number)
  if request.method == 'POST':
    form = VendorForm(request.POST, instance=vendor)
    if form.is_valid():
      print ("form is valid, update db?")
      form.save()
      return HttpResponseRedirect(reverse('vendors'))
  else:
    form = VendorForm(instance=vendor)
  context = {
      'form': form,
      'vendor_id': vendor_number,
      'current_event': get_current_event().event_name,
      'current_user': request.user,
      }
  return render(request, 'baskets/vendor_detail.html', context)


@login_required
def detail(request, basket_id):
  if request.method == 'POST':
    form = AddItemForm(request.POST)
    if form.is_valid():
      #print ("form is valid")
      basket = get_object_or_404(Basket, pk=basket_id)
      vendor = get_object_or_404(Vendor, vendor_number=request.POST['vendor'])
      item = Item(basket=basket, vendorID=vendor, price=request.POST['price'], created_by=request.user)
      item.save()
    else:
      print ("form is not valid")
  else:
    form = AddItemForm()
### The following fails, if there are no items assigned to a basket. We do
### not want this behavior.
#  item_list = get_list_or_404(Item, basket=basket_id)
  item_list = Item.objects.filter(basket=basket_id).order_by('-created')
  basket_sum = Item.objects.filter(basket=basket_id).aggregate(Sum('price'))
  context = {
      'form': form,
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
  vendor = get_object_or_404(Vendor, vendor_number=request.POST['vendorID'])
  item = Item(basket=basket, vendorID=vendor,
      price=request.POST['price'],created_by=request.user)
  item.save()
  return HttpResponseRedirect(reverse('detail', args=(basket.id,)))


@login_required
def add_basket(request):
  basket = Basket(created_by=request.user, event=get_current_event())
  basket.save()
  return HttpResponseRedirect(reverse('detail', args=(basket.id,)))


# @login_required
# def vendors_to_pdf(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
# 
#     buffer = BytesIO()
# 
#     # Create the PDF object, using the BytesIO object as its "file."
#     p = canvas.Canvas(buffer)
# 
#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawString(100, 100, "Hello world.")
# 
#     # Close the PDF object cleanly.
#     p.showPage()
#     p.save()
# 
#     # Get the value of the BytesIO buffer and write it to the response.
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#     return response
