from django import forms
from .models import ContactSubmission
from .models import ApplicationSubmission
from .models import CareerSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "contact_number", "query"]
        
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = ApplicationSubmission
        # We don't include source_page here, because we'll set it automatically
        fields = ["name", "phone", "email", "course_option"]
        
        
        
        

class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerSubmission
        fields = ["name", "email", "number", "position"]