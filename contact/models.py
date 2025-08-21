from django.db import models
from wagtail.admin.panels import FieldPanel

class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20, blank=True)
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("email"),
        FieldPanel("contact_number"),
        FieldPanel("query"),
        # FieldPanel("created_at"),
    ]

    def __str__(self):
        return f"Submission from {self.name} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"
        ordering = ["-created_at"]
        
        
        
        
        
# --- Add this new model to contact/models.py ---

class ApplicationSubmission(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    course_option = models.CharField(max_length=255)
    # This will automatically record which course page the form was submitted from
    source_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("course_option"),
        FieldPanel("source_page"),
        # FieldPanel("created_at"),
    ]

    def __str__(self):
        return f"Application from {self.name} for {self.course_option}"

    class Meta:
        verbose_name = "Course Application Submission"
        verbose_name_plural = "Course Application Submissions"
        ordering = ["-created_at"]
        
        
        
        
        
class CareerSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    position = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("email"),
        FieldPanel("number"),
        FieldPanel("position"),
    ]

    def __str__(self):
        return f"Career application from {self.name} for {self.position}"

    class Meta:
        verbose_name = "Career Submission"
        verbose_name_plural = "Career Submissions"
        ordering = ["-created_at"]