from .cart import Cart


def cart_cp(request):
    return {'cart': Cart(request)}