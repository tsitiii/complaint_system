
from django.core.validators import RegexValidator
from django.db import models

from django.contrib.auth.models import AbstractUser

class GovernmentOrganization(models.Model):
    CATEGORY_CHOICES = (
        ('sanitation', 'Sanitation'),
        ('roads', 'Roads and Infrastructure'),
        ('water', 'Water Supply'),
        ('electricity', 'Electricity'),
        ('health', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES) 
    jurisdiction = models.CharField(max_length=100,verbose_name="" )
    description = models.TextField(blank=True, verbose_name="Area of Responisibility")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('gov_org', 'Government Organization'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    full_name = models.CharField(max_length=100,db_index=True)
    ethiopian_phone_validator = RegexValidator(
        regex=r'^(\+2519\d{8}|09\d{8}|2519\d{8})$',
        message="Enter a valid Ethiopian phone number (09XXXXXXXX, +2519XXXXXXXX, or 2519XXXXXXXX)."
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        validators=[ethiopian_phone_validator]
    )
    organization = models.ForeignKey( GovernmentOrganization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )

    def __str__(self):
        return self.full_name