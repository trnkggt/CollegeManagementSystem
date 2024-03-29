from decimal import Decimal
from django.conf import settings

from courses.models import Course


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart


    def add(self, course):
        """
        Add a course to cart
        """
        course_id = str(course.id)
        if course_id not in self.cart:
            self.cart[course_id] = {
                'title': course.title,
                'price': str(course.price),
                'quantity': 1
            }

        self.save()


    def remove(self, course):
        """
        Remove a course from cart
        """
        course_id = str(course.id)
        if course_id in self.cart:
            del self.cart[course_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and get the courses
        from database.
        """
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        cart = self.cart.copy()
        for course in courses:
            cart[str(course.id)]['course'] = course
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())

    def __len__(self):
        return len([item for item in self.cart.values()])

    def clear(self):
        """
        Remove cart from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()