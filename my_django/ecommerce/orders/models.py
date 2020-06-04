from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
from carts.models import Cart


User = get_user_model()

STATUS_CHOICES = (
		("Đang xử lý", "Đang xử lý"),
		("Đang vận chuyển", "Đang vận chuyển"),
		("Đã giao hàng", "Đã giao hàng"),
	)

#python tuples

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	order_id = models.CharField(max_length=120, default='ABC', unique=True)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
	# address **
	sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
	tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
	final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.order_id