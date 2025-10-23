from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import (
    City,
    Service,
    CityService,
    Lead,
    NewsletterSubscriber,
    ResourceDownload,
    BlogPost,
    BlogCategory
)
from .forms import ContactForm, NewsletterForm


def home(request):
    """
    View for the homepage with tech-themed hero section
    """
    # Get featured services
    services = Service.objects.filter(is_active=True).order_by('display_order')[:6]
    
    # Get featured cities
    cities = City.objects.filter(is_active=True)[:6]
    
    # Get featured blog posts
    blog_posts = BlogPost.objects.filter(is_published=True, featured=True)[:3]
    
    # If we don't have enough featured posts, get recent posts
    if len(blog_posts) < 3:
        remaining_count = 3 - len(blog_posts)
        recent_posts = BlogPost.objects.filter(
            is_published=True
        ).exclude(
            id__in=[post.id for post in blog_posts]
        ).order_by('-created_at')[:remaining_count]
        
        blog_posts = list(blog_posts) + list(recent_posts)
    
    # Handle newsletter subscription form on homepage
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': 'Easyian - Innovative Technology Services',
        'meta_description': 'Leading provider of technology solutions including software development, website development, CRM, HRMS, autodialer, and more.',
        'newsletter_form': newsletter_form,
        'services': services,
        'cities': cities,
        'blog_posts': blog_posts,
    }
    return render(request, 'home.html', context)


def services(request):
    """
    View for listing all services
    """
    services_list = Service.objects.filter(is_active=True).order_by('display_order')
    
    context = {
        'page_title': 'Our Services | Easyian',
        'meta_description': 'Explore our range of professional technology services designed to help your business grow and succeed.',
        'services': services_list,
    }
    return render(request, 'services/services.html', context)


def service_detail(request, service_slug):
    """
    View for individual service detail page
    """
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    
    # Get cities where this service is available
    service_cities = City.objects.filter(
        services__service=service,
        services__is_active=True,
        is_active=True
    ).distinct()
    
    # Handle newsletter subscription form
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('service_detail', service_slug=service_slug)
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': service.meta_title,
        'meta_description': service.meta_description,
        'service': service,
        'service_cities': service_cities,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'services/service_detail.html', context)


def city_list(request):
    """
    View for listing all cities
    """
    cities = City.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_title': 'Cities We Serve | Easyian',
        'meta_description': 'Discover our technology services available across major cities in India.',
        'cities': cities,
    }
    return render(request, 'cities/city_list.html', context)


def city_home(request, city_slug):
    """
    View for city landing page
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    
    # Get services available in this city
    city_services = CityService.objects.filter(
        city=city,
        service__is_active=True,
        is_active=True
    ).select_related('service').order_by('service__display_order')
    
    # Get blog posts specific to this city
    blog_posts = BlogPost.objects.filter(
        city=city,
        is_published=True
    ).order_by('-created_at')[:3]
    
    # Handle newsletter subscription form
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        form_data = request.POST.copy()
        form_data['city'] = city.id
        newsletter_form = NewsletterForm(form_data)
        if newsletter_form.is_valid():
            subscriber = newsletter_form.save(commit=False)
            subscriber.city = city
            subscriber.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('city_home', city_slug=city_slug)
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': f"Easyian Technology Services in {city.name}",
        'meta_description': f"Professional technology solutions in {city.name}. Software development, website development, CRM, and more for businesses in {city.name}.",
        'city': city,
        'city_services': city_services,
        'blog_posts': blog_posts,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'cities/city_home.html', context)


def city_services(request, city_slug):
    """
    View for services available in a specific city
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    
    # Get services available in this city
    city_services = CityService.objects.filter(
        city=city,
        service__is_active=True,
        is_active=True
    ).select_related('service').order_by('service__display_order')
    
    context = {
        'page_title': f"Our Services in {city.name} | Easyian",
        'meta_description': f"Explore our range of technology services available in {city.name}. Professional solutions for businesses of all sizes.",
        'city': city,
        'city_services': city_services,
    }
    return render(request, 'cities/city_services.html', context)


def city_service_detail(request, service_slug, city_slug):
    """
    View for service detail in specific city
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    
    try:
        city_service = CityService.objects.get(
            city=city,
            service=service,
            is_active=True
        )
    except CityService.DoesNotExist:
        # If this service isn't explicitly set up for this city,
        # redirect to the general service page
        return redirect('service_detail', service_slug=service_slug)
    
    # Handle contact form
    if request.method == 'POST' and 'contact_submit' in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            lead = contact_form.save(commit=False)
            lead.city = city
            lead.specific_service = service
            lead.interest = service.slug if service.slug in [choice[0] for choice in Lead.INTEREST_CHOICES] else 'other'
            lead.source = 'city_page'
            lead.save()
            messages.success(request, "Thank you for your message. Our team will contact you shortly.")
            return redirect('city_service_detail', service_slug=service_slug, city_slug=city_slug)
    else:
        contact_form = ContactForm()
    
    # Handle newsletter subscription
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        form_data = request.POST.copy()
        newsletter_form = NewsletterForm(form_data)
        if newsletter_form.is_valid():
            subscriber = newsletter_form.save(commit=False)
            subscriber.city = city
            subscriber.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('city_service_detail', service_slug=service_slug, city_slug=city_slug)
    else:
        newsletter_form = NewsletterForm()
    
    context = {
        'page_title': city_service.meta_title if city_service.meta_title else f"{service.title} Services in {city.name} | Easyian",
        'meta_description': city_service.meta_description if city_service.meta_description else f"Professional {service.title} services in {city.name}. Expert solutions tailored for local businesses.",
        'city': city,
        'service': service,
        'city_service': city_service,
        'contact_form': contact_form,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'cities/city_service_detail.html', context)


def city_contact(request, city_slug):
    """
    View for city-specific contact page
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    
    # Handle contact form
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            lead = contact_form.save(commit=False)
            lead.city = city
            lead.source = 'city_page'
            lead.save()
            messages.success(request, "Thank you for your message. Our team will contact you shortly.")
            return redirect('city_contact', city_slug=city_slug)
    else:
        contact_form = ContactForm()
    
    context = {
        'page_title': f"Contact Us in {city.name} | Easyian",
        'meta_description': f"Get in touch with our {city.name} team for expert technology solutions tailored to your business needs.",
        'city': city,
        'contact_form': contact_form,
    }
    return render(request, 'cities/city_contact.html', context)


def city_blog(request, city_slug):
    """
    View for city-specific blog posts
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    
    # Get blog posts for this city
    blog_posts = BlogPost.objects.filter(
        city=city,
        is_published=True
    ).order_by('-created_at')
    
    # Set up pagination
    paginator = Paginator(blog_posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': f"Blog | Easyian {city.name}",
        'meta_description': f"Read our latest insights, news, and articles specific to {city.name}. Technology trends, tips, and success stories.",
        'city': city,
        'page_obj': page_obj,
    }
    return render(request, 'cities/city_blog.html', context)


def blog_list(request):
    """
    View for the blog listing page
    """
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    categories = BlogCategory.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    
    # Set up pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Blog | Easyian',
        'meta_description': 'Explore our blog for insights, tech news, tips, and updates from our team of experts.',
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """
    View for individual blog post
    """
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts with improved logic
    related_posts = []
    
    # First, try to get posts from the same category
    same_category_posts = BlogPost.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id).order_by('-created_at', '-views')[:3]
    
    related_posts.extend(same_category_posts)
    
    # If we don't have enough posts from same category, get from other categories
    if len(related_posts) < 3:
        remaining_count = 3 - len(related_posts)
        other_posts = BlogPost.objects.filter(
            is_published=True
        ).exclude(
            id__in=[p.id for p in related_posts] + [post.id]
        ).order_by('-created_at', '-views')[:remaining_count]
        
        related_posts.extend(other_posts)
    
    # If still no posts, get any published posts (excluding current)
    if len(related_posts) == 0:
        related_posts = BlogPost.objects.filter(
            is_published=True
        ).exclude(id=post.id).order_by('-created_at')[:3]
    
    context = {
        'page_title': post.title + ' | Easyian Blog',
        'meta_description': post.summary,
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/blog_detail.html', context)


def blog_category(request, category_slug):
    """
    View for posts in a specific category
    """
    category = get_object_or_404(BlogCategory, slug=category_slug)
    posts = BlogPost.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')
    
    # Set up pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': f'{category.name} | Easyian Blog',
        'meta_description': f'Read our articles about {category.name}. Latest insights and expert advice.',
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/blog_category.html', context)


def landing(request):
    """Landing page for Facebook/Meta ads"""
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            lead = contact_form.save(commit=False)
            lead.source = 'landing_page'
            lead.save()
            messages.success(request, "Thank you! We'll get back to you within 24 hours.")
            return redirect('contact_success')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        contact_form = ContactForm()

    return render(request, 'landing.html', {'contact_form': contact_form})


def contact(request):
    """Simple contact form view"""
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            lead = contact_form.save(commit=False)
            lead.source = 'contact_form'
            lead.save()
            messages.success(request, "Thank you! We'll get back to you within 24 hours.")
            return redirect('contact_success')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        contact_form = ContactForm()

    return render(request, 'contact.html', {'contact_form': contact_form})


def contact_success(request):
    """
    View for contact form success
    """
    return render(request, 'contact_success.html', {
        'page_title': 'Message Sent | Easyian',
    })


def about(request):
    """
    View for the about page
    """
    # Team members data - in a real application, this might come from a database
    team_members = [
        {
            'name': 'John Smith',
            'position': 'CEO & Founder',
            'bio': 'With over 15 years of experience in technology leadership, John has driven innovation across multiple industries.',
            'image': 'team/john-smith.jpg',
        },
        {
            'name': 'Sarah Johnson',
            'position': 'CTO',
            'bio': 'Sarah brings extensive expertise in software architecture and emerging technologies to lead our technical strategy.',
            'image': 'team/sarah-johnson.jpg',
        },
        {
            'name': 'Michael Chen',
            'position': 'Head of Product',
            'bio': "Michael's background in user experience and product development ensures our solutions deliver exceptional value.",
            'image': 'team/michael-chen.jpg',
        },
        {
            'name': 'Emily Rodriguez',
            'position': 'Lead Developer',
            'bio': 'Emily specializes in full-stack development and has led numerous successful projects for enterprise clients.',
            'image': 'team/emily-rodriguez.jpg',
        },
    ]
    
    # Company milestones - in a real application, this might come from a database
    milestones = [
        {
            'year': 2015,
            'title': 'Company Founded',
            'description': 'Easyian was established with a mission to deliver innovative technology solutions.',
        },
        {
            'year': 2017,
            'title': 'Expanded Service Offerings',
            'description': 'Added CRM and HRMS solutions to our portfolio of services.',
        },
        {
            'year': 2019,
            'title': 'Launched Training Academy',
            'description': 'Introduced comprehensive tech courses to help professionals advance their careers.',
        },
        {
            'year': 2022,
            'title': 'National Expansion',
            'description': 'Expanded our services to major cities across India.',
        },
    ]
    
    context = {
        'page_title': 'About Us | Easyian',
        'meta_description': 'Learn about Easyian, our mission, values, team, and the technology solutions we provide to clients nationwide.',
        'team_members': team_members,
        'milestones': milestones,
    }
    return render(request, 'about.html', context)


def privacy_policy(request):
    """
    View for privacy policy page
    """
    return render(request, 'legal/privacy_policy.html', {
        'page_title': 'Privacy Policy | Easyian',
    })


def terms_of_service(request):
    """
    View for terms of service page
    """
    return render(request, 'legal/terms_of_service.html', {
        'page_title': 'Terms of Service | Easyian',
    })


@require_POST
def newsletter_signup(request):
    """
    View for handling newsletter signups
    """
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Thank you for subscribing to our newsletter!")
    else:
        # If email already exists, still show success message to avoid revealing subscribed emails
        if 'email' in form.errors and 'already exists' in str(form.errors['email']):
            messages.success(request, "Thank you for subscribing to our newsletter!")
        else:
            messages.error(request, "There was an error with your submission. Please try again.")
    
    # Redirect back to the page they came from
    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    return redirect('home')


# API Endpoints for frontend interactions

def api_cities(request):
    """
    API endpoint for getting city data
    """
    cities = City.objects.filter(is_active=True).order_by('name').values('name', 'slug', 'state')
    return JsonResponse({'cities': list(cities)})


def api_services(request):
    """
    API endpoint for getting service data
    """
    services = Service.objects.filter(is_active=True).order_by('display_order').values(
        'id', 'title', 'slug', 'short_description'
    )
    return JsonResponse({'services': list(services)})


def api_city_services(request, city_slug):
    """
    API endpoint for getting services available in a specific city
    """
    try:
        city = City.objects.get(slug=city_slug, is_active=True)
    except City.DoesNotExist:
        return JsonResponse({'error': 'City not found'}, status=404)
    
    city_services = CityService.objects.filter(
        city=city,
        service__is_active=True,
        is_active=True
    ).select_related('service').order_by('service__display_order')
    
    services_data = []
    for cs in city_services:
        services_data.append({
            'id': cs.service.id,
            'title': cs.service.title,
            'slug': cs.service.slug,
            'short_description': cs.service.short_description,
            'url': f"/{cs.service.slug}-services-in-{city.slug}/"
        })
    
    return JsonResponse({
        'city': {
            'name': city.name,
            'slug': city.slug,
            'state': city.state
        },
        'services': services_data
    })