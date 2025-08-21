from django.shortcuts import render
from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock

from contact.forms import ContactForm

# --- All previous blocks are here, unchanged ---
class HeroCardBlock(blocks.StructBlock):#...
    icon = blocks.CharBlock(required=False, help_text="Add an emoji or icon character. e.g. 💻, 🚀, 📊")
    title = blocks.CharBlock(required=False, max_length=100)
    description = blocks.TextBlock(required=False, max_length=200)
    class Meta:
        template = "blocks/homepage/hero_card_block.html"
        icon = 'form'
        label = 'Hero Floating Card'
class FeatureCardBlock(blocks.StructBlock):#...
    icon = blocks.CharBlock(required=True, help_text="Add an emoji or icon character. e.g. 🎯, 🏭, 🤝")
    title = blocks.CharBlock(required=True, max_length=100)
    description = blocks.TextBlock(required=True, max_length=255)
    class Meta:
        template = "blocks/homepage/feature_card_block.html"
        icon = 'star'
        label = 'Feature Card'
class SolutionCardBlock(blocks.StructBlock):#...
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True)
    text = blocks.TextBlock(required=True)
    link_page = blocks.PageChooserBlock(required=False)
    class Meta:
        template = "blocks/homepage/solution_card_block.html"
        icon = "pick"
        label = "Solution Card"
class PartnerLogoBlock(blocks.StructBlock):#...
    logo_image = ImageChooserBlock(required=True)
    partner_name = blocks.CharBlock(required=True, help_text="For alt text and internal reference")
    class Meta:
        template = "blocks/homepage/partner_logo_block.html"
        icon = 'image'
        label = "Partner Logo"
class TestimonialBlock(blocks.StructBlock):#...
    image = ImageChooserBlock(required=True)
    quote = blocks.TextBlock(required=True, help_text="The person's testimonial.")
    author_name = blocks.CharBlock(required=True)
    author_role = blocks.CharBlock(required=False, help_text="e.g., Digital Finance or Kerala, India")
    class Meta:
        template = "blocks/homepage/testimonial_block.html"
        icon = "openquote"
        label = "Testimonial"
        
class CourseCardBlock(blocks.StructBlock):
    # ... and replace it with this:
    
    # CHANGED: Use ImageChooserBlock instead of CharBlock
    icon = ImageChooserBlock(required=False, help_text="Upload an icon for the course.")
    
    tags = blocks.CharBlock(required=False, help_text="Comma-separated categories, e.g., Popular, Cloud, Web Dev")
    title = blocks.CharBlock(required=True, max_length=100)
    description = blocks.TextBlock(required=True, max_length=255)
    duration = blocks.CharBlock(required=True, max_length=100)
    price = blocks.CharBlock(required=True, max_length=50)

    # NEW: Add a PageChooserBlock to link the card
    link_page = blocks.PageChooserBlock(required=False, help_text="Select a detail page for this course.")

    class Meta:
        template = "blocks/homepage/course_card_block.html"
        icon = 'education'
        label = 'Course Card'
        
class TabContentCardBlock(blocks.StructBlock):#...
    header_title = blocks.CharBlock()
    header_subtitle = blocks.CharBlock(required=False)
    icon = ImageChooserBlock()
    text = blocks.TextBlock()
    button_text = blocks.CharBlock(default="Explore")
    button_link = blocks.PageChooserBlock(required=False)
    class Meta:
        template = "blocks/homepage/tab_content_card_block.html"
        icon = "form"
        label = "Tab Content Card"
class TabItemBlock(blocks.StructBlock):#...
    tab_title = blocks.CharBlock()
    tab_icon = ImageChooserBlock(required=False)
    cards = blocks.ListBlock(TabContentCardBlock())
class TabbedContentBlock(blocks.StructBlock):#...
    tabs = blocks.ListBlock(TabItemBlock())
    class Meta:
        template = "blocks/homepage/tabbed_content_block.html"
        icon = "tab"
        label = "Tabbed Content Section"
class HeroBlock(blocks.StructBlock):#...
    title = blocks.CharBlock(required=False, help_text="Add <strong> tags for bold text")
    image = ImageChooserBlock(required=False)
    class Meta:
        template = "blocks/standardpage/hero_block.html"
        icon = "image"
        label = "Hero Section"
class TwoColumnTextBlock(blocks.StructBlock):#...
    left_column_title = blocks.CharBlock(required=False, help_text="Use <br> for line breaks")
    right_column_title = blocks.CharBlock(required=False)
    right_column_text = RichTextBlock(required=False)
    class Meta:
        template = "blocks/standardpage/two_column_text_block.html"
        icon = "grip"
        label = "Two Column Text"
class CenteredTextWithImageBlock(blocks.StructBlock):#...
    title = blocks.CharBlock(required=False)
    text = RichTextBlock(required=False)
    image = ImageChooserBlock(required=False)
    class Meta:
        template = "blocks/standardpage/centered_text_with_image_block.html"
        icon = "image"
        label = "Centered Text w/ Image"
class FullWidthCtaBlock(blocks.StructBlock):#...
    title = blocks.CharBlock(required=False, help_text="Use <br> for line breaks")
    text = RichTextBlock(required=False)
    class Meta:
        template = "blocks/standardpage/full_width_cta_block.html"
        icon = "arrows-up-down"
        label = "Full Width CTA"
class IconCardBlock(blocks.StructBlock):#...
    icon = ImageChooserBlock(required=False)
    title = blocks.CharBlock(required=False, help_text="Use <br> for line breaks")
    text = RichTextBlock(required=False)
    class Meta:
        template = "blocks/standardpage/icon_card_block.html"
        icon = "cog"
        label = "Icon Card"
class IconGridBlock(blocks.StructBlock):#...
    title = blocks.CharBlock()
    cards = blocks.ListBlock(IconCardBlock())
    class Meta:
        template = "blocks/standardpage/icon_grid_block.html"
        icon = "table"
        label = "Icon Grid Section"
class ContactFormBlock(blocks.StructBlock):#...
    left_column_title = blocks.CharBlock(default="Get In Touch With Us!")
    left_column_text = RichTextBlock()
    form_title = blocks.CharBlock(default="QUICK CONTACT")
    class Meta:
        template = "blocks/shared/contact_form_block.html"
        icon = "form"
        label = "Contact Form Section"
class RecruitmentHeroBlock(blocks.StructBlock):#...
    title = blocks.CharBlock(help_text="Use <br> for line breaks")
    image = ImageChooserBlock()
    class Meta:
        template = "blocks/recruitment_page/hero_block.html"
        icon = "image"
        label = "Hero Section (Recruitment)"
class TwoColumnContentBlock(blocks.StructBlock):#...
    left_column_title = blocks.CharBlock(help_text="Use <br> for line breaks")
    right_column_text = RichTextBlock()
    class Meta:
        template = "blocks/recruitment_page/two_column_content_block.html"
        icon = "grip"
        label = "Two Column Content (Recruitment)"
class TalentListBlock(blocks.StructBlock):#...
    title = blocks.CharBlock(help_text="Use <br> for line breaks")
    talent_list = RichTextBlock(features=['ul'], help_text="Use a bulleted list.")
    background_image = ImageChooserBlock()
    class Meta:
        template = "blocks/recruitment_page/talent_list_block.html"
        icon = "list-ul"
        label = "Talent Professionals List"
class StatsBlock(blocks.StructBlock):#...
    left_column_title = blocks.CharBlock(help_text="Use <br> for line breaks")
    stats_left = RichTextBlock()
    stats_right = blocks.ListBlock(
        blocks.StructBlock([('percentage', blocks.CharBlock()), ('label', blocks.CharBlock())])
    )
    class Meta:
        template = "blocks/recruitment_page/stats_block.html"
        icon = "order"
        label = "Student Profile / Stats"
class FourIconColumnBlock(blocks.StructBlock):#...
    title = blocks.CharBlock()
    columns = blocks.ListBlock(
        blocks.StructBlock([('icon', ImageChooserBlock()), ('title', blocks.CharBlock()), ('text', blocks.TextBlock())])
    )
    class Meta:
        template = "blocks/recruitment_page/four_icon_column_block.html"
        icon = "table"
        label = "Why Hire From Us (4 Columns)"

# --- NEW Blocks for the Consulting Page ---
class ConsultingHeroBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text="Use <br> for line breaks")
    image = ImageChooserBlock()
    class Meta:
        template = "blocks/consulting_page/hero_block.html"
        icon = "image"
        label = "Hero (Consulting)"

class ConsultingIntroBlock(blocks.StructBlock):
    text = RichTextBlock(features=['bold', 'italic', 'link'])
    class Meta:
        template = "blocks/consulting_page/intro_block.html"
        icon = "pilcrow"
        label = "Intro Paragraph (Consulting)"

class ServiceItemBlock(blocks.StructBlock):
    icon = ImageChooserBlock()
    title = blocks.CharBlock()
    text = RichTextBlock()
    class Meta:
        icon = "cog"
        label = "Service Item"

class ConsultingMainContentBlock(blocks.StructBlock):
    background_image = ImageChooserBlock()
    services = blocks.ListBlock(ServiceItemBlock())
    class Meta:
        template = "blocks/consulting_page/main_content_block.html"
        icon = "grip"
        label = "Main Content (Consulting)"

# --- Page Models ---
class HomePageStat(Orderable):#...
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='hero_stats')
    stat_number = models.CharField(max_length=50)
    stat_label = models.CharField(max_length=100)
    panels = [ FieldPanel('stat_number'), FieldPanel('stat_label'), ]
class HomePage(Page):#...
    template = "home/home_page.html"
    hero_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = RichTextField(blank=True)
    hero_primary_button_text = models.CharField(max_length=50)
    hero_secondary_button_text = models.CharField(max_length=50)
    body = StreamField([
        ('hero_cards', blocks.ListBlock(HeroCardBlock())),
        ('features_section', blocks.StructBlock([('title', blocks.CharBlock()), ('subtitle', blocks.TextBlock()), ('features', blocks.ListBlock(FeatureCardBlock()))], template="blocks/features_section.html")),
        ('solutions_section', blocks.StructBlock([('title', blocks.CharBlock()), ('solutions', blocks.ListBlock(SolutionCardBlock()))], template="blocks/solutions_section.html")),
        ('tabbed_content', TabbedContentBlock()),
        ('partners_section', blocks.StructBlock([('title', blocks.CharBlock()), ('logos', blocks.ListBlock(PartnerLogoBlock()))], template="blocks/partners_section.html")),
        ('testimonials_section', blocks.StructBlock([('title', blocks.CharBlock()), ('testimonials', blocks.ListBlock(TestimonialBlock()))], template="blocks/testimonials_section.html")),
        ('courses_section', blocks.StructBlock([('title', blocks.CharBlock()), ('subtitle', blocks.TextBlock()), ('courses', blocks.ListBlock(CourseCardBlock()))], template="blocks/courses_section.html")),
        ('contact_form', ContactFormBlock()),
        ('cta_section', blocks.StructBlock([('title', blocks.CharBlock()), ('description', blocks.TextBlock()), ('button_text', blocks.CharBlock())], template="blocks/cta_section.html")),
    ], use_json_field=True, null=True, blank=True)
    content_panels = Page.content_panels + [ MultiFieldPanel([FieldPanel('hero_title'), FieldPanel('hero_subtitle'), FieldPanel('hero_primary_button_text')], heading="Hero Section"), MultiFieldPanel([InlinePanel('hero_stats', label="Hero Stat")], heading="Hero Statistics"), FieldPanel('body'), ]
    def serve(self, request, *args, **kwargs):#...
        context = self.get_context(request, *args, **kwargs)
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                context['form_success'] = True
                form = ContactForm()
        else:
            form = ContactForm()
        context['form'] = form
        return render(request, self.template, context)
class StandardPage(Page):#...
    body = StreamField([
        ('hero', HeroBlock()), ('two_columns', TwoColumnTextBlock()), ('centered_text_image', CenteredTextWithImageBlock()), ('full_width_cta', FullWidthCtaBlock()), ('icon_grid', IconGridBlock()),
    ], use_json_field=True, blank=True)
    content_panels = Page.content_panels + [ FieldPanel('body') ]
class RecruitmentPage(Page):#...
    template = "home/recruitment_page.html"
    body = StreamField([
        ('hero', RecruitmentHeroBlock()),
        ('two_column_content', TwoColumnContentBlock()),
        ('talent_list', TalentListBlock()),
        ('stats', StatsBlock()),
        ('four_columns', FourIconColumnBlock()),
    ], use_json_field=True, blank=True)
    content_panels = Page.content_panels + [ FieldPanel('body') ]

# --- NEW Consulting Page Model ---
class ConsultingPage(Page):
    template = "home/consulting_page.html"

    body = StreamField([
        ('hero', ConsultingHeroBlock()),
        ('intro', ConsultingIntroBlock()),
        ('main_content', ConsultingMainContentBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]