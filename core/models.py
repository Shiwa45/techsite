# models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class City(models.Model):
    """
    Model to represent cities where services are offered
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    state = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='cities/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"Professional Services in {self.name} | Easyian"
        if not self.meta_description:
            self.meta_description = f"Discover Easyian's premium technology services in {self.name}. Expert solutions for businesses of all sizes."
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('city_home', kwargs={'city_slug': self.slug})


class Service(models.Model):
    """
    Model to represent services/products offered
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    long_description = models.TextField()
    icon_path = models.CharField(max_length=500, blank=True)  # SVG path for icons
    features = models.JSONField(default=list)  # Store as JSON array
    benefits = models.JSONField(default=list)
    process = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    featured_image = models.ImageField(upload_to='services/', blank=True, null=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = f"{self.title} | Easyian"
        if not self.meta_description:
            self.meta_description = f"Professional {self.title} services from Easyian. {self.short_description}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'service_slug': self.slug})


class CityService(models.Model):
    """
    Junction model linking cities and services with city-specific content
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='cities')
    custom_content = models.TextField(blank=True)  # City-specific service content
    custom_features = models.JSONField(default=list, blank=True)
    custom_benefits = models.JSONField(default=list, blank=True)
    success_stories = models.JSONField(default=list, blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('city', 'service')
        verbose_name = 'City Service'
        verbose_name_plural = 'City Services'
        ordering = ['city__name', 'service__display_order']
    
    def __str__(self):
        return f"{self.service.title} in {self.city.name}"
    
    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = f"{self.service.title} Services in {self.city.name} | Easyian"
        if not self.meta_description:
            self.meta_description = f"Professional {self.service.title} services in {self.city.name}. Expert solutions tailored for local businesses."
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('city_service_detail', kwargs={
            'service_slug': self.service.slug,
            'city_slug': self.city.slug
        })


# Keep existing models

class Lead(models.Model):
    """
    Model to store leads generated from the website
    """
    INTEREST_CHOICES = [
        ('software_dev', 'Software Development Service'),
        ('website_dev', 'Website Development'),
        ('crm', 'CRM Solution'),
        ('hrms', 'HRMS Solution'),
        ('voip', 'VOIP Service'),
        ('api', 'API Development'),
        ('autodialer', 'Autodialer Solution'),
        ('other', 'Other'),
    ]
    
    SOURCE_CHOICES = [
        ('contact_form', 'Contact Form'),
        ('newsletter', 'Newsletter Signup'),
        ('download', 'Resource Download'),
        ('webinar', 'Webinar Registration'),
        ('demo', 'Demo Request'),
        ('city_page', 'City Page'),
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
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES, default='other')
    specific_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
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
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscribers')
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
    related_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='resources')
    
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
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
    related_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
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