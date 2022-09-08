from django.db import models
from django.shortcuts import render

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.blocks import RawHTMLBlock
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.search.models import Query


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]


class Student(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

class Sveden(Page):
    body = StreamField([
        ('HTML', RawHTMLBlock())
    ], blank=True)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
class Abiturient(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]


#функция поиска

def search(request):
    # Search
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = Page.objects.live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Render template
    return render(request, 'search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })