from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock
from django.shortcuts import render
from contact.forms import CareerForm
from django.http import JsonResponse
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from wagtail.images.models import Image

# --- Blocks for the Company Page Builder ---

class PlacedStudentBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    name = blocks.CharBlock(required=False)
    role = blocks.CharBlock(required=False)
    company = blocks.CharBlock(required=False)
    
    class Meta:
        icon = "user"
        label = "Placed Student"

class PlacementsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, default="Placements")
    students = blocks.ListBlock(PlacedStudentBlock(), required=False)

    class Meta:
        template = "blocks/company_page/placements_block.html"
        icon = "users"
        label = "Placements Section"

class CareersFormBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, default="CAREERS")
    subtitle = blocks.TextBlock(required=False)
    email_info = RichTextBlock(required=False, help_text="e.g., Please share your resume with hr@techno.academy")

    class Meta:
        template = "blocks/company_page/careers_form_block.html"
        icon = "form"
        label = "Careers Form"

class OpenPositionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    # THIS IS THE FIX:
    position_count = blocks.CharBlock(max_length=50, required=False) 
    apply_link = blocks.URLBlock(required=False)
    # For Booleans in blocks, 'required=False' is enough
    is_highlighted = blocks.BooleanBlock(default=False, required=False, help_text="Check to make this position stand out with a dark background.")

    class Meta:
        label = "Open Position"

class OpenPositionsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, default="OPEN POSITIONS")
    positions = blocks.ListBlock(OpenPositionBlock(), required=False)

    class Meta:
        template = "blocks/company_page/open_positions_block.html"
        icon = "list-ul"
        label = "Open Positions"

class GalleryImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    label = blocks.CharBlock(required=False)
    button_text = blocks.CharBlock(required=False, default="More Photos")
    link_page = blocks.PageChooserBlock(required=False)
    
    class Meta:
        label = "Gallery Image"

class PhotoGalleryBlock(blocks.StructBlock):
    images = blocks.ListBlock(GalleryImageBlock(), required=False)
    
    class Meta:
        template = "blocks/company_page/photo_gallery_block.html"
        icon = "image"
        label = "Photo Gallery"



    
    
    
class GalleryPageImage(Orderable):
    page = ParentalKey('company.GalleryPage', on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

class GalleryPage(Page):
    template = "company/gallery_page.html"

    hero_image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )
    intro_title = models.CharField(max_length=255)
    tag = models.CharField(max_length=100, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_image'),
        FieldPanel('intro_title'),
        FieldPanel('tag'),
        InlinePanel('gallery_images', label="Gallery Images"),
    ]
    
    
class IntroBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    subtitle = blocks.TextBlock(required=False)

    class Meta:
        template = "blocks/company_page/intro_block.html"
        icon = "pilcrow"
        label = "Intro Section"
        
        
        
# --- The Main Company Page Model ---
class CompanyPage(Page):
    template = "company/company_page.html"
    
    # Hero image can be a simple field on the page model itself
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('intro', IntroBlock()),
        ('placements', PlacementsBlock()),
        ('careers_form', CareersFormBlock()),
        ('open_positions', OpenPositionsBlock()),
        ('photo_gallery', PhotoGalleryBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_image'),
        FieldPanel('body'),
    ]
    
    def serve(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if request.method == 'POST':
            form = CareerForm(request.POST)
            if form.is_valid():
                form.save()

                if is_ajax:
                    return JsonResponse({'success': True})
                
                context['career_form_success'] = True
                form = CareerForm()
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': form.errors})
        else:
            form = CareerForm()
            
        context['career_form'] = form
        return render(request, self.template, context)