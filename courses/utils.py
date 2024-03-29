
def is_teacher(user):
    """
    Check if user is in teacher's group.
    """
    return user.groups.filter(name='Teachers').exists()

def is_admin(user):
    """
    Check if user has is_staff=True
    """
    return user.is_staff