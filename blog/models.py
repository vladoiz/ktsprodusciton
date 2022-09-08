from django.db import models


from modelcluster.fields import ParentalKey
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from django.shortcuts import render

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)


    @property
    def blogs(self):
        # Получить список страниц блога, которые являются потомками этой страницы
        blogs = BlogPage.objects.live().descendant_of(self)

        # Сортировать по дате
        blogs = blogs.order_by('-date')

        return blogs

    def get_context(self, request):
        blogs = self.blogs
        
        # Обновить контекст шаблона
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

    def get_context(self, request):
        context = super().get_context(request)

        # Get blog entries
        blog_entries = BlogPage.objects.child_of(self).live()

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blog_entries = blog_entries.filter(tags__name=tag)

        context['blog_entries'] = blog_entries
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', on_delete=models.CASCADE, related_name='tagged_items')

class BlogPage(Page):
        date = models.DateField("Post date")
        intro = models.CharField(max_length=250)
        body = RichTextField(blank=True)
        bg_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+')
        tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

        promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
        ]

        def main_image(self):
         gallery_item = self.gallery_images.first()
         if gallery_item:
            return gallery_item.image
         else:
            return None

        search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

        content_panels = Page.content_panels + [
            FieldPanel('date'),
            FieldPanel('intro'),
            ImageChooserPanel('bg_image'),
            FieldPanel('body', classname="full"),
            InlinePanel('gallery_images', label="Gallery images"),
        ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]