from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.models import Image

class WebinarCard(Orderable):
    page = ParentalKey('webinar.WebinarPage', on_delete=models.CASCADE, related_name='webinar_cards')
    
    tag = models.CharField(max_length=100, default="FREE LIVE webinar session")
    trainer_image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )
    trainer_name = models.CharField(max_length=255)
    trainer_role = models.CharField(max_length=255)
    workshop_title = models.CharField(max_length=255)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    is_expired = models.BooleanField(default=False)
    apply_link = models.URLField(blank=True)

    panels = [
        FieldPanel('tag'),
        FieldPanel('trainer_image'),
        FieldPanel('trainer_name'),
        FieldPanel('trainer_role'),
        FieldPanel('workshop_title'),
        FieldPanel('date'),
        FieldPanel('time'),
        FieldPanel('is_expired'),
        FieldPanel('apply_link'),
    ]

class WebinarPage(Page):
    template = "webinar/webinar_page.html"
    
    # Hero Section
    hero_image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )
    title_override = models.CharField(max_length=255, blank=True, help_text="Optional. If blank, the page title will be used.")
    subtitle = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_image'),
            FieldPanel('title_override'),
            FieldPanel('subtitle'),
        ], heading="Hero Section"),

        MultiFieldPanel([
            InlinePanel('webinar_cards', label="Webinar Card")
        ], heading="Webinar Cards"),
    ]