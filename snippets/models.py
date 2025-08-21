from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class CourseOption(models.Model):
    name = models.CharField(max_length=255) # e.g., "Cloud Computing"
    
    panels = [FieldPanel('name')]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course Option for Forms"
        verbose_name_plural = "Course Options for Forms"