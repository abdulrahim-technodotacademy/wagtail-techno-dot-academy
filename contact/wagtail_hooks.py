from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import ContactSubmission
from .models import ApplicationSubmission
from .models import CareerSubmission

class ContactSubmissionAdmin(ModelAdmin):
    model = ContactSubmission
    menu_label = "Submissions"
    menu_icon = "mail"
    list_display = ("name", "email", "contact_number", "created_at")
    search_fields = ("name", "email", "query")

modeladmin_register(ContactSubmissionAdmin)



class ApplicationSubmissionAdmin(ModelAdmin):
    model = ApplicationSubmission
    menu_label = "Applications" # This will create a new menu item
    menu_icon = "user"
    list_display = ("name", "course_option", "source_page", "created_at")
    search_fields = ("name", "email", "course_option")

modeladmin_register(ApplicationSubmissionAdmin)



class CareerSubmissionAdmin(ModelAdmin):
    model = CareerSubmission
    menu_label = "Careers" # This will create a new top-level menu item
    menu_icon = "user"
    list_display = ("name", "position", "email", "created_at")
    search_fields = ("name", "email", "position")

modeladmin_register(CareerSubmissionAdmin)