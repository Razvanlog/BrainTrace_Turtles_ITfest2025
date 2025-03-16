from django import forms
from .models import PatientData

class PatientDataForm(forms.ModelForm):
    class Meta:
        model = PatientData
        fields = [
            "salutation", "first_name", "last_name", "email", "phone_number", 
            "birth_date", "address", "country", "tumor_image", "medical_info", 
            "communication_preference"
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "tumor_image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "medical_info": forms.ClearableFileInput(attrs={"accept": "application/pdf,.csv,.xls,.xlsx"}),
        }
