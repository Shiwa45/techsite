from django.contrib import admin
from django.utils.html import format_html
from .models import (
    City,
    Service,
    CityService,
    Lead,
    NewsletterSubscriber,
    ResourceDownload,
    BlogCategory,
    BlogPost,
    BlogSection
)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'is_active', 'service_count')
    list_filter = ('state', 'is_active')
    search_fields = ('name', 'state')
    prepopulated_fields = {'slug': ('name',)}
    
    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = 'Services'


class CityServiceInline(admin.TabularInline):
    model = CityService
    extra = 1
    fields = ('city', 'is_active', 'custom_content')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'currency', 'display_order', 'is_active', 'city_count')
    list_filter = ('is_active',)
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CityServiceInline]
    
    def city_count(self, obj):
        return obj.cities.count()
    city_count.short_description = 'Cities'


class CityServiceAdmin(admin.ModelAdmin):
    list_display = ('service', 'city', 'is_active')
    list_filter = ('service', 'city', 'is_active')
    search_fields = ('service__title', 'city__name', 'custom_content')
    

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'interest', 'city', 'specific_service', 'status', 'created_at')
    list_filter = ('status', 'interest', 'source', 'city', 'specific_service', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company', 'job_title', 'city')
        }),
        ('Interest', {
            'fields': ('interest', 'specific_service', 'message')
        }),
        ('Lead Details', {
            'fields': ('source', 'status', 'notes')
        }),
    )


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'city', 'is_active', 'created_at')
    list_filter = ('is_active', 'city', 'created_at')
    search_fields = ('email', 'name')
    date_hierarchy = 'created_at'


@admin.register(ResourceDownload)
class ResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'related_service', 'download_count', 'created_at')
    list_filter = ('resource_type', 'related_service', 'created_at')
    search_fields = ('title', 'description')
    

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


class BlogSectionInline(admin.StackedInline):
    model = BlogSection
    extra = 1
    fields = ('section_type', 'heading', 'heading_level', 'content', 'image', 'image_caption',
              'video_url', 'code_language', 'list_items', 'order')

    class Media:
        css = {
            'all': ('admin/css/blog_section.css',)
        }


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'city', 'related_service', 'is_published',
                    'featured', 'views', 'reading_time', 'created_at')
    list_filter = ('is_published', 'featured', 'category', 'author', 'city', 'related_service', 'published_at')
    search_fields = ('title', 'summary', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [BlogSectionInline]
    readonly_fields = ('views', 'created_at', 'updated_at', 'reading_time')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'author', 'featured_image', 'summary')
        }),
        ('Main Content', {
            'fields': ('content',),
            'description': 'Main content or introduction. Use sections below for structured content.'
        }),
        ('Author Information', {
            'fields': ('author_bio', 'author_image'),
            'classes': ('collapse',)
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'reading_time', 'tags'),
            'classes': ('collapse',)
        }),
        ('Relationships', {
            'fields': ('city', 'related_service'),
            'classes': ('collapse',)
        }),
        ('Publishing Options', {
            'fields': ('is_published', 'featured', 'published_at', 'views', 'created_at', 'updated_at')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields


@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'section_type', 'heading', 'order')
    list_filter = ('section_type', 'blog_post')
    search_fields = ('heading', 'content', 'blog_post__title')
    list_editable = ('order',)
    ordering = ('blog_post', 'order')


# Register CityService
admin.site.register(CityService, CityServiceAdmin)