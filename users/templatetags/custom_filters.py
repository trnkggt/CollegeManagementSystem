from django import template


register = template.Library()

@register.filter(name='user_is_teacher')
def user_is_teacher(user):
    return user.groups.filter(name='Teachers').exists()

@register.filter(name='model_name')
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None