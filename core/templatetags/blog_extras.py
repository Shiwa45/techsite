# core/templatetags/blog_extras.py
from django import template
import re
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def reading_time(content):
    """
    Calculate estimated reading time for blog content
    Average reading speed: 200 words per minute
    """
    if not content:
        return 1
    
    # Strip HTML tags and get plain text
    text = strip_tags(content)
    
    # Count words (split by whitespace)
    word_count = len(text.split())
    
    # Calculate reading time (minimum 1 minute)
    reading_time_minutes = max(1, round(word_count / 200))
    
    return reading_time_minutes

@register.filter
def truncate_words_html(value, arg):
    """
    Truncate HTML content while preserving tags
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    
    # Strip HTML for word counting
    text = strip_tags(value)
    words = text.split()
    
    if len(words) <= length:
        return value
    
    # Truncate and add ellipsis
    truncated_words = words[:length]
    return ' '.join(truncated_words) + '...'

@register.filter
def get_category_color(category_name):
    """
    Get color class for category badges
    """
    color_map = {
        'technology': 'blue',
        'business': 'green', 
        'development': 'purple',
        'design': 'pink',
        'marketing': 'yellow',
        'security': 'red',
        'cloud': 'indigo',
        'ai': 'cyan',
        'mobile': 'orange',
        'web': 'teal',
    }
    
    category_slug = category_name.lower().replace(' ', '-')
    return color_map.get(category_slug, 'gray')

@register.simple_tag
def get_featured_posts(limit=3):
    """
    Get featured blog posts
    """
    from core.models import BlogPost
    return BlogPost.objects.filter(is_published=True, featured=True).order_by('-created_at')[:limit]

@register.simple_tag  
def get_recent_posts(limit=5):
    """
    Get recent blog posts
    """
    from core.models import BlogPost
    return BlogPost.objects.filter(is_published=True).order_by('-created_at')[:limit]

@register.simple_tag
def get_popular_posts(limit=5):
    """
    Get popular blog posts by view count
    """
    from core.models import BlogPost
    return BlogPost.objects.filter(is_published=True).order_by('-views')[:limit]

@register.simple_tag
def get_posts_by_category(category_slug, limit=5):
    """
    Get posts by category
    """
    from core.models import BlogPost, BlogCategory
    try:
        category = BlogCategory.objects.get(slug=category_slug)
        return BlogPost.objects.filter(
            category=category, 
            is_published=True
        ).order_by('-created_at')[:limit]
    except BlogCategory.DoesNotExist:
        return BlogPost.objects.none()

@register.inclusion_tag('blog/tags/related_posts.html')
def show_related_posts(post, limit=3):
    """
    Show related posts based on category and tags
    """
    from core.models import BlogPost
    
    # Get posts from same category
    related_posts = BlogPost.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id).order_by('-created_at')[:limit]
    
    return {'related_posts': related_posts}

@register.inclusion_tag('blog/tags/post_tags.html')
def show_post_tags(post):
    """
    Display post tags
    """
    return {'tags': post.get_tag_list()}

@register.filter
def add_nofollow(value):
    """
    Add nofollow to external links in content
    """
    import re
    
    # Pattern to match external links
    pattern = r'<a\s+(?:[^>]*?\s+)?href="(https?://[^"]*)"'
    
    def add_nofollow_to_match(match):
        url = match.group(1)
        full_match = match.group(0)
        
        # Don't add nofollow to internal links (you can customize the domain)
        if 'easyian.com' in url or url.startswith('/'):
            return full_match
        
        # Add nofollow and target="_blank" to external links
        if 'rel=' not in full_match:
            return full_match.replace('>', ' rel="nofollow noopener" target="_blank">')
        else:
            return full_match
    
    return re.sub(pattern, add_nofollow_to_match, value)