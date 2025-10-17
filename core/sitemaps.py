"""
Sitemaps for the website to improve SEO
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import City, Service, CityService, BlogPost, BlogCategory


class StaticSitemap(Sitemap):
    """
    Sitemap for static pages
    """
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['home', 'about', 'contact', 'services', 'blog_list']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    """
    Sitemap for service pages
    """
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('service_detail', kwargs={'service_slug': obj.slug})


class CitySitemap(Sitemap):
    """
    Sitemap for city landing pages
    """
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return City.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('city_home', kwargs={'city_slug': obj.slug})


class CityServiceSitemap(Sitemap):
    """
    Sitemap for city-service pages
    """
    changefreq = "monthly"
    priority = 0.9  # Highest priority for these pages

    def items(self):
        return CityService.objects.filter(
            is_active=True,
            service__is_active=True,
            city__is_active=True
        )

    def location(self, obj):
        return reverse('city_service_detail', kwargs={
            'service_slug': obj.service.slug,
            'city_slug': obj.city.slug
        })


class BlogSitemap(Sitemap):
    """
    Sitemap for blog posts
    """
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


class BlogCategorySitemap(Sitemap):
    """
    Sitemap for blog categories
    """
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return BlogCategory.objects.all()

    def location(self, obj):
        return reverse('blog_category', kwargs={'category_slug': obj.slug})