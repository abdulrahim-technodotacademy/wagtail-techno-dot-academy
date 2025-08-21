from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("level_1_items", label="Level 1 Items (e.g., Topics)")
    ]

    def __str__(self):
        return self.title

class Level1MenuItem(Orderable, ClusterableModel):
    menu = ParentalKey(Menu, on_delete=models.CASCADE, related_name="level_1_items")
    link_title = models.CharField(max_length=100, blank=True)
    # Level 1 items usually don't link anywhere, but we can keep it optional
    link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel("link_title"),
        PageChooserPanel("link_page"),
        InlinePanel("level_2_items", label="Level 2 Items (e.g., Cloud)")
    ]

    @property
    def url(self): return self.link_page.url if self.link_page else '#'
    @property
    def title(self): return self.link_title or (self.link_page.title if self.link_page else '')

class Level2MenuItem(Orderable, ClusterableModel):
    parent = ParentalKey(Level1MenuItem, on_delete=models.CASCADE, related_name="level_2_items")
    link_title = models.CharField(max_length=100, blank=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel("link_title"),
        PageChooserPanel("link_page"),
        InlinePanel("level_3_items", label="Level 3 Items (e.g., Cloud Computing)")
    ]

    @property
    def url(self): return self.link_page.url if self.link_page else '#'
    @property
    def title(self): return self.link_title or (self.link_page.title if self.link_page else '')

class Level3MenuItem(Orderable, ClusterableModel):
    parent = ParentalKey(Level2MenuItem, on_delete=models.CASCADE, related_name="level_3_items")
    link_title = models.CharField(max_length=100, blank=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel("link_title"),
        PageChooserPanel("link_page"),
        InlinePanel("level_4_items", label="Level 4 Items (Final Links)")
    ]

    @property
    def url(self): return self.link_page.url if self.link_page else '#'
    @property
    def title(self): return self.link_title or (self.link_page.title if self.link_page else '')

class Level4MenuItem(Orderable):
    parent = ParentalKey(Level3MenuItem, on_delete=models.CASCADE, related_name="level_4_items")
    link_title = models.CharField(max_length=100, blank=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        PageChooserPanel("link_page"),
        FieldPanel("link_title"),
    ]

    @property
    def url(self): return self.link_page.url if self.link_page else '#'
    @property
    def title(self): return self.link_title or (self.link_page.title if self.link_page else '')
    
    
    
    
class FooterLink(Orderable):
    column = ParentalKey("FooterColumn", on_delete=models.CASCADE, related_name="footer_links")
    link_title = models.CharField(max_length=100)
    link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    
    panels = [
        FieldPanel("link_title"),
        PageChooserPanel("link_page"),
    ]

class FooterColumn(Orderable, ClusterableModel):
    footer = ParentalKey("Footer", on_delete=models.CASCADE, related_name="footer_columns")
    title = models.CharField(max_length=100)

    panels = [
        FieldPanel("title"),
        InlinePanel("footer_links", label="Links")
    ]

@register_snippet
class Footer(ClusterableModel):
    title = models.CharField(max_length=100) # For internal reference, e.g., "Main Footer"
    
    panels = [
        FieldPanel("title"),
        InlinePanel("footer_columns", label="Footer Columns")
    ]

    def __str__(self):
        return self.title