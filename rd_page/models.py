from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock

# --- Blocks for the R&D Page Builder ---

class RdHeroBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        template = "blocks/rd_page/rd_hero_block.html"  
        icon = "image"
        label = "R&D Hero"

class IntroTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    # FIXED: Added the missing RichTextField for the intro text
    text = RichTextBlock(features=['bold', 'italic', 'link'], required=False)

    class Meta:
        template = "blocks/rd_page/intro_text_block.html"
        icon = "pilcrow"
        label = "Intro Text"

class ImageTextAlternatingBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(required=False)
    # FIXED: Added the missing RichTextField for the main text
    text = RichTextBlock(features=['bold', 'italic', 'link'], required=False)
    image_alignment = blocks.ChoiceBlock(
        choices=[('left', 'Image on Left'), ('right', 'Image on Right')],
        default='left',
        label="Image Alignment"
    )

    class Meta:
        template = "blocks/rd_page/image_text_alternating_block.html"
        icon = "grip"
        label = "Image & Text (Alternating)"

class IconCardGridItemBlock(blocks.StructBlock):
    icon = ImageChooserBlock()
    title = blocks.CharBlock()
    text = RichTextBlock(features=['bold', 'italic', 'link'])

    class Meta:
        label = "Grid Card"

class IconCardGridBlock(blocks.StructBlock):
    # This block doesn't need a title itself, the section template will have one
    cards = blocks.ListBlock(IconCardGridItemBlock())

    class Meta:
        template = "blocks/rd_page/icon_card_grid_block.html"
        icon = "table"
        label = "Icon Card Grid (Teal Section)"


# --- The Main R&D Page Model ---
class RdPage(Page):
    template = "rd_page/rd_page.html"

    body = StreamField([
        ('hero', RdHeroBlock()),
        ('intro_text', IntroTextBlock()),
        ('image_text', ImageTextAlternatingBlock()),
        ('icon_grid', IconCardGridBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]