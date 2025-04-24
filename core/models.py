# models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class Lead(models.Model):
    """
    Model to store leads generated from the website
    """
    INTEREST_CHOICES = [
        ('digital_marketing', 'Digital Marketing Course'),
        ('full_stack', 'Full Stack Development Course'),
        ('software_dev', 'Software Development Service'),
        ('crm', 'CRM Solution'),
        ('hrms', 'HRMS Solution'),
        ('voip', 'VOIP Service'),
        ('api', 'API Development'),
        ('autodialer', 'Autodialer Solution'),
        ('website_dev', 'Website Development'),
        ('other', 'Other'),
    ]
    
    SOURCE_CHOICES = [
        ('contact_form', 'Contact Form'),
        ('newsletter', 'Newsletter Signup'),
        ('download', 'Resource Download'),
        ('webinar', 'Webinar Registration'),
        ('demo', 'Demo Request'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES, default='other')
    message = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='contact_form')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_interest_display()})"


class NewsletterSubscriber(models.Model):
    """
    Model to store newsletter subscribers
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.email


class ResourceDownload(models.Model):
    """
    Model to track resource downloads for lead generation
    """
    RESOURCE_TYPES = [
        ('ebook', 'E-book'),
        ('whitepaper', 'Whitepaper'),
        ('case_study', 'Case Study'),
        ('template', 'Template'),
        ('guide', 'Guide'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/')
    description = models.TextField()
    
    # Lead generation requirements
    require_name = models.BooleanField(default=True)
    require_email = models.BooleanField(default=True)
    require_phone = models.BooleanField(default=False)
    require_company = models.BooleanField(default=False)
    
    # Statistics
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    



class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    summary = models.TextField(max_length=300)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=300, blank=True, help_text="Separate tags with commas")
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def get_tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
