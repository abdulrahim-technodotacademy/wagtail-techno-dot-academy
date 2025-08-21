from django import template
from snippets.models import CourseOption

register = template.Library()

@register.inclusion_tag('tags/course_options_dropdown.html')
def get_course_options():
    options = CourseOption.objects.all()
    return {'options': options}