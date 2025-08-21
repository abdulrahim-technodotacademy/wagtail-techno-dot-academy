from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
# ADD THIS IMPORT
from wagtail.images.models import Image

@register_setting
class SiteSettings(BaseSiteSetting):
    # ADD THE NEW FIELD
    light_logo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="The logo to display when light mode is active. Should be dark text on a transparent background."
    )
    
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Your WhatsApp number in international format, e.g., 919876543210 (without '+')"
    )
    whatsapp_prefilled_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional: The default message that will appear when a user clicks the button."
    )

    # UPDATE THE PANELS
    panels = [
        MultiFieldPanel([
            FieldPanel("light_logo"),
        ], heading="Logos"),
        
        MultiFieldPanel([
            FieldPanel("whatsapp_number"),
            FieldPanel("whatsapp_prefilled_text"),
        ], heading="Contact Information"),
    ]

    class Meta:
        verbose_name = "Site Settings"