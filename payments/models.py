from django.db import models
from django.conf import settings

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL,
                             null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s order"

    def get_total_cost(self):
        return sum(item.get_price for item in self.items.all())

    def get_stripe_url(self):
        if not self.stripe_id:
            # no payment id
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for payments
            path = '/test/'
        else:
            # Real payment path
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items')
    course = models.ForeignKey('courses.Course',
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def get_price(self):
        return self.price