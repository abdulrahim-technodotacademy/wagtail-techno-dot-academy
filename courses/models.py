from django.db import models

from wagtail.models import Page, Orderable, ParentalKey
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock
# NEW: Import for linking to documents
from wagtail.documents.blocks import DocumentChooserBlock
from django.shortcuts import render
from contact.forms import ApplicationForm
from django.http import JsonResponse

# --- Blocks for the Course Page ---

class CourseHeroBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    tag = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    description = RichTextBlock(required=False)
    duration = blocks.CharBlock(required=False)
    mode = blocks.CharBlock(required=False)
    eligibility = blocks.CharBlock(required=False)
    certifications = blocks.ListBlock(ImageChooserBlock(label="Certification Logo", required=False),required=False)
    apply_button_text = blocks.CharBlock(default="Apply Now", required=False)
    # FIXED: Was models.CharField, now blocks.CharBlock
    phone_number = blocks.CharBlock(max_length=20, required=False) 
    
    class Meta:
        template = "blocks/course_page/hero_block.html"
        icon = "image"
        label = "Course Hero"

class LearningTabItemBlock(blocks.StructBlock):
    tab_title = blocks.CharBlock(required=False)
    tab_subtitle = blocks.CharBlock(required=False)
    content_list = RichTextBlock(features=['ul'], help_text="Use a bulleted list.", required=False)
    
    class Meta:
        label = "Learning Tab Item"

class LearningTabsBlock(blocks.StructBlock):
    tabs = blocks.ListBlock(LearningTabItemBlock(), required=False)

    class Meta:
        template = "blocks/course_page/learning_tabs_block.html"
        icon = "tab"
        label = "Learning Tabs Section"

class FutureStatsBannerBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    stats = blocks.ListBlock(
        blocks.StructBlock([
            ('value', blocks.CharBlock(required=False)),
            ('label', blocks.CharBlock(required=False)),
        ]), required=False
    )

    class Meta:
        template = "blocks/course_page/stats_banner_block.html"
        icon = "order"
        label = "Future Stats Banner"

class ProvidersVideoBlock(blocks.StructBlock):
    main_title = blocks.CharBlock(required=False, label="Main Section Title")
    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    logos = blocks.ListBlock(
    ImageChooserBlock(label="Provider Logo", required=False),
    required=False
)

    video_thumbnail = ImageChooserBlock(required=False)
    video_url = blocks.URLBlock(required=False)
    enquire_button_text = blocks.CharBlock(default="Enquire Now", required=False)
    brochure_button_text = blocks.CharBlock(default="Download Brochure", required=False)
    # NEW: Field for the downloadable brochure
    brochure_file = DocumentChooserBlock(required=False)
    
    class Meta:
        template = "blocks/course_page/providers_video_block.html"
        icon = "media"
        label = "Providers & Video"

class ContactBannerBlock(blocks.StructBlock):
    contact_one_flag = ImageChooserBlock(required=False)
    contact_one_phone = blocks.CharBlock(max_length=20, required=False)
    contact_one_email = blocks.EmailBlock(required=False)
    contact_two_flag = ImageChooserBlock(required=False)
    contact_two_phone = blocks.CharBlock(max_length=20, required=False)
    contact_two_email = blocks.EmailBlock(required=False)

    class Meta:
        template = "blocks/course_page/contact_banner_block.html"
        icon = "call"
        label = "Contact Banner"





class CertificationCardBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(required=False)
    button_text = blocks.CharBlock(default="Know More", required=False)
    button_link = blocks.PageChooserBlock(required=False)
    class Meta:
        icon = "badge"
        label = "Certification Card"

class CertificationsGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Courses / Certifications", required=False)
    cards = blocks.ListBlock(CertificationCardBlock(), required=False)
    class Meta:
        template = "blocks/course_page/certifications_grid_block.html"
        icon = "table"
        label = "Certifications Grid"


class TrainingDetailItemBlock(blocks.StructBlock):
    item = RichTextBlock(features=['ul'])
    class Meta:
        label = "Detail Item"

class TrainingDetailsBlock(blocks.StructBlock):
    main_logo = ImageChooserBlock(required=False)
    main_title = blocks.CharBlock(required=False)
    
    # Three columns of details
    left_column_title = blocks.CharBlock(required=False)
    left_column_items = blocks.ListBlock(RichTextBlock(features=['ul'], label="Detail Item", required=False), required=False)
    
    middle_column_title = blocks.CharBlock(required=False) # NEW
    middle_column_items = blocks.ListBlock(RichTextBlock(features=['ul'], label="Detail Item", required=False), required=False)

    right_column_title = blocks.CharBlock(required=False)
    right_column_items = blocks.ListBlock(RichTextBlock(features=['ul'], label="Detail Item", required=False), required=False)

    class Meta:
        template = "blocks/course_page/training_details_block.html"
        icon = "grip"
        label = "Training Details"



class LocationCardBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    location_name = blocks.CharBlock(required=False, help_text="e.g., CALICUT, INDIA")
    office_name = blocks.CharBlock(required=False, default="TECHNO DOT ACADEMY")
    address = RichTextBlock(required=False)
    phone = blocks.CharBlock(required=False)
    email = blocks.EmailBlock(required=False)

    class Meta:
        label = "Location Card"
        
        
        
class LocationsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, default="VISIT US")
    locations = blocks.ListBlock(LocationCardBlock())

    class Meta:
        template = "blocks/course_page/locations_block.html"
        icon = "site"
        label = "Locations Section"



# in courses/models.py

class SyllabusHeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(label="Heading")
    class Meta:
        template = "blocks/course_page/syllabus_heading_block.html"
        icon = "title"
        label = "Syllabus Heading"

class SyllabusListBlock(blocks.StructBlock):
    items = RichTextBlock(features=['ul'], label="List Items")
    class Meta:
        template = "blocks/course_page/syllabus_list_block.html"
        icon = "list-ul"
        label = "Syllabus List"

# This is the new, final version of the SyllabusBlock
class SyllabusBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, default="What You Will Learn")
    subtitle = blocks.TextBlock(required=False, help_text="A short subtitle to display under the main title.")
    
    # THIS IS THE FIX: We use blocks.StreamBlock, NOT fields.StreamField
    left_column = blocks.StreamBlock([
        ('heading', SyllabusHeadingBlock()),
        ('list', SyllabusListBlock()),
    ], use_json_field=True, required=False)
    
    right_column = blocks.StreamBlock([
        ('heading', SyllabusHeadingBlock()),
        ('list', SyllabusListBlock()),
    ], use_json_field=True, required=False)

    class Meta:
        template = "blocks/course_page/syllabus_block.html"
        icon = "list-ul"
        label = "Syllabus / What You Learn"

# --- NEW Block for "At a Glance" Section ---
class GlanceItemBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    label = blocks.CharBlock(required=False, help_text="e.g., Level, Product")
    value = blocks.CharBlock(required=False, help_text="e.g., Beginner, Azure")
    class Meta:
        label = "Glance Item"

class GlanceBlock(blocks.StructBlock):
    tag = blocks.CharBlock(required=False, help_text="The small tag above the main title.")
    title = blocks.CharBlock(required=False, default="Microsoft Certified: Azure Administrator Associate")
    subtitle = blocks.TextBlock(required=False)
    glance_title = blocks.CharBlock(required=False, default="At a glance")
    items = blocks.ListBlock(GlanceItemBlock())

    class Meta:
        template = "blocks/course_page/glance_block.html"
        icon = "view"
        label = "At a Glance Section"



# --- The Main Course Page Model ---
class CoursePage(Page):
    template = "courses/course_page.html"
    
    body = StreamField([
        ('hero', CourseHeroBlock()),
        ('learning_tabs', LearningTabsBlock()),
        ('stats_banner', FutureStatsBannerBlock()),
        ('syllabus', SyllabusBlock()),
        ('at_a_glance', GlanceBlock()),
        ('program_info', blocks.StructBlock([
        ('title', blocks.CharBlock(required=False)),
        ('subtitle', blocks.CharBlock(required=False)),
        ('text', RichTextBlock(required=False)),
    ], icon="pilcrow", label="Program Info Section", template="blocks/course_page/program_info_block.html")),
        ('providers_video', ProvidersVideoBlock()),
        ('contact_banner', ContactBannerBlock()),
        ('certifications_grid', CertificationsGridBlock()),
        ('training_details', TrainingDetailsBlock()),
        ('providers_video', ProvidersVideoBlock()),
        ('locations', LocationsBlock()),
        ('contact_banner', ContactBannerBlock()),
    ], use_json_field=True, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        
        MultiFieldPanel([
            InlinePanel('accreditations', label="Accreditation")
        ], heading="Accreditations (Below Hero)"),
    ]
        # --- ADD THIS ENTIRE METHOD ---
    def serve(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        
        # Check if it's an AJAX request (from our form script)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.source_page = self
                submission.save()

                if is_ajax:
                    return JsonResponse({'success': True})
                
                context['application_success'] = True
                form = ApplicationForm()
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': form.errors})
        else:
            form = ApplicationForm()
            
        context['application_form'] = form
        return render(request, self.template, context)
    
    
class CourseAccreditation(Orderable):
    page = ParentalKey('courses.CoursePage', on_delete=models.CASCADE, related_name='accreditations')
    icon = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )
    text = models.CharField(max_length=100)

    panels = [
        FieldPanel('icon'),
        FieldPanel('text'),
    ]
    
    
    
