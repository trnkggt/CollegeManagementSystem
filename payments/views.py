from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from decimal import Decimal

from courses.models import Course
from .cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_completed

from users.models import StudentProfile, CourseBuying

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
def add_to_cart(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)

    cart.add(course=course)
    messages.success(request, 'Course added to your cart')

    return redirect('course_detail', course_id)

@require_POST
def cart_remove(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course=course)
    messages.success(request, 'Course removed from your cart')
    return redirect('payments:cart')

@require_POST
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Cart has been cleared')
    return redirect('payments:cart')

def view_cart(request):
    cart = Cart(request)

    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def order_create(request):
    cart = Cart(request)
    user = request.user
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    course=item['course'],
                    price=item['price']
                )
            success_url = request.build_absolute_uri(
                reverse('payments:completed')
            )
            cancel_url = request.build_absolute_uri(
                reverse('payments:canceled')
            )
            session_data = {
                'mode': 'payment',
                'client_reference_id': order.id,
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
            }
            for item in order.items.all():
                session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.course.title,
                        },
                    },
                    'quantity': 1
                })

            session = stripe.checkout.Session.create(**session_data)

            return redirect(session.url, code=303)
            # return redirect(reverse('payments:process'))
    else:
        form = OrderCreateForm(instance=user)

    return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})
# @require_POST
# def payment(request):
#     order_id = request.session.get('order_id', None)
#     order = get_object_or_404(Order, id=order_id)
#     success_url = request.build_absolute_uri(
#         reverse('payment:completed')
#     )
#     cancel_url = request.build_absolute_uri(
#         reverse('payment:canceled')
#     )
#     session_data = {
#         'mode': 'payment',
#         'client_reference_id': order.id,
#         'success_url': success_url,
#         'cancel_url': cancel_url,
#         'line_items': []
#     }
#     for item in order.items.all():
#         session_data['line_items'].append({
#             'price_data': {
#                 'unit_amount': int(item.price * Decimal('100')),
#                 'currency': 'usd',
#                 'product_data': item.course.title,
#             }
#         })
#
#     session = stripe.checkout.Session.create(**session_data)
#
#     return redirect(session.url, code=303)

def payment_completed(request):
    cart = Cart(request)
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    order_completed.delay(request.user.first_name, request.user.email)
    for item in cart:
        CourseBuying.objects.create(
            student=student_profile,
            course=item['course']
        )
        student_profile.courses.add(item['course'])
    student_profile.save()
    cart.clear()
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')