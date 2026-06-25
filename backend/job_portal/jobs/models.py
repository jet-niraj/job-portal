from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class Job(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('posted', 'Posted'),
        ('filled', 'Filled'),
    ]
    
    CATEGORY_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('intern', 'Intern'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
    ]
    
    # Basic Information
    job_title = models.CharField(
        max_length=255,
        help_text="Title of the job posting"
    )
    
    description = models.TextField(
        help_text="Detailed job description"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Current status of the job posting"
    )
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text="Type of employment"
    )
    
    # Location Information
    address = models.CharField(
        max_length=255,
        help_text="Job location address"
    )
    
    city = models.CharField(
        max_length=100,
        help_text="City"
    )
    
    state = models.CharField(
        max_length=100,
        help_text="State/Province"
    )
    
    # Duration
    start_date = models.DateField(
        help_text="Job start date"
    )
    
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Job end date (optional)"
    )
    
    # Job Profile Picture
    job_profile_picture = models.ImageField(
        upload_to='job_images/%Y/%m/%d/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        help_text="Profile picture for the job posting"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date when job was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date when job was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['city']),
            models.Index(fields=['state']),
            models.Index(fields=['job_title']),
        ]
    
    def __str__(self):
        return f"{self.job_title} - {self.status}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")