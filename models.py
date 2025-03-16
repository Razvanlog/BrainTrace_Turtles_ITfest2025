from django.db import models
from django.utils.text import slugify
import os

# ✅ Helper function to save files in user-specific folders
def patient_directory_path(instance, filename):
    """Uploads files to media/tumor_images/{first_last}/{filename}"""
    name_slug = slugify(f"{instance.first_name}_{instance.last_name}")
    return f"tumor_images/{name_slug}/{filename}"

def medical_directory_path(instance, filename):
    """Uploads medical files to media/medical_files/{first_last}/{filename}"""
    name_slug = slugify(f"{instance.first_name}_{instance.last_name}")
    return f"medical_files/{name_slug}/{filename}"

class PatientData(models.Model):
    SALUTATION_CHOICES = [
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
        ('Mrs.', 'Mrs.'),
        ('Dr.', 'Dr.'),
        ('Prof.', 'Prof.'),
    ]

    COMMUNICATION_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('phone', 'Phone Call'),
        ('whatsapp', 'WhatsApp'),
    ]

    salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, blank=True, default="")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")
    
    # ✅ File upload paths use user-based directory structure
    tumor_image = models.ImageField(upload_to=patient_directory_path, blank=True, null=True)
    medical_info = models.FileField(upload_to=medical_directory_path, blank=True, null=True)

    # ✅ Supports multiple choices for communication (optional)
    communication_preference = models.CharField(
        max_length=50,
        choices=COMMUNICATION_CHOICES,
        blank=True,
        default=""
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
