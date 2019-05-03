from django import template

register = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None

@register.filter
def enrolled(course, user_id):
    if course.students.filter(id=user_id).exists():
        return True
    return False

