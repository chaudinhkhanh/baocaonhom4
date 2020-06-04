import stripe
import random
import hashlib

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from django.template.loader import render_to_string


# Create your models here.



stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


class UserStripe(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	stripe_id = models.CharField(max_length=120, null=True, blank=True)

	def __unicode__(self):
		return str(self.stripe_id)


def get_create_stripe(user):
	new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
	if created:
		customer = stripe.Customer.create(
  			email = str(user.email)
		)
		new_user_stripe.stripe_id = customer.id
		new_user_stripe.save()

def user_created(sender, instance, created, *args, **kwargs):
	user = instance
	#
	if created:
		get_create_stripe(user)
		email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
		if email_is_created:
			short_hash =  hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:5]
			base, domain = str(user.email).split("@")
			activation_key = hashlib.sha256(short_hash+base).encode('utf8').hexdigest()
			email_confirmed.activation_key = activation_key
			email_confirmed.save()
			email_confirmed.activate_user_email()



post_save.connect(user_created, sender=User)



class EmailConfirmed(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	activation_key = models.CharField(max_length=200)
	confirmed = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.confirmed)

	def activate_user_email(self):
		#send email here & render a string
		activation_url = "http://localhost:8000/accounts/activate/%s" %(self.activation_key)
		context = {
			"activation_key": self.activation_key,
			"activation_url": activation_url,
			"user": self.user.username,
		}
		message = render_to_string("accounts/activation_message.txt", context)
		subject = "Activate your Email"
		self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
		#self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

	def email_user(self, subject, message, from_email=None, *kwargs):
		send_mail(subject, message, from_email, [self.user.email], kwargs)

class UserAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	address = models.CharField(max_length=120)
	address2 = models.CharField(max_length=120, null=True, blank=True)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=120, null=True, blank=True)
	country = models.CharField(max_length=120)
	zipcode = models.CharField(max_length=25)
	phone =  models.CharField(max_length=120)
	shipping = models.BooleanField(default=True)
	billing = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.user.username)