from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaksbr

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    """Convert text to HTML with basic formatting"""
    # Simple text-to-HTML conversion (for now, can be enhanced with markdown library later)
    return mark_safe(linebreaksbr(text))


@register.filter(name='reading_time')
def reading_time(content):
    """Calculate reading time based on content"""
    if not content:
        return 1
    word_count = len(str(content).split())
    return max(1, round(word_count / 200))


@register.inclusion_tag('blog/tags/section_renderer.html')
def render_section(section):
    """Render a blog section based on its type"""
    return {'section': section}


@register.simple_tag
def generate_toc(sections):
    """Generate table of contents from blog sections"""
    toc = []
    for section in sections:
        if section.section_type == 'heading' and section.heading:
            toc.append({
                'id': f"section-{section.order}",
                'title': section.heading,
                'level': section.heading_level
            })
    return toc
