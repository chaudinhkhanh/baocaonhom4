import time

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect

# Create your views here.

from accounts.forms import UserAddressForm
from accounts.models import UserAddress
from carts.models import Cart

from .models import Order
from .utils import id_generator

def orders(request):
	context = {}
	template = "orders/user.html"
	return render(request, template, context)


#require user login ** 
@login_required
def checkout(request):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
		#return HttpResponseRedirect("/cart/")
		return HttpResponseRedirect(reverse("cart"))
	
	try:
		new_order = Order.objects.get(cart=cart)
	except Order.DoesNotExist:
		new_order = Order()
		new_order.cart = cart
		new_order.user = request.user
		new_order.order_id = id_generator()
		new_order.save()
	except:
		# work on some error message
		return HttpResponseRedirect(reverse("cart"))

	address_form = UserAddressForm(request.POST or None)
	if address_form.is_valid():
		new_address = address_form.save(commit=False)
		new_address.user = request.user
		new_address.save()

	#assign address
	#run credit card
	if new_order.status == "Đã giao hàng":
		#cart.delete()
		del request.session['cart_id']
		del request.session['items_total']
		return HttpResponseRedirect(reverse("cart"))

	context = {"address_form": address_form}
	template = "orders/checkout.html"

	return render(request, template, context)