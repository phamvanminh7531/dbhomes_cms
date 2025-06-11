from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from django.db import models
from wagtail.snippets.models import register_snippet
from django.utils.text import slugify
from modelcluster.fields import ParentalManyToManyField
from django.shortcuts import get_object_or_404
from django import forms
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from streams.blocks import HeroSectionBlock
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@register_snippet
class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=False, blank=False,
        on_delete=models.CASCADE,
        related_name='+'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('image'),
    ]

    def __str__(self):
        return self.name



@register_snippet
class ProductTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class ProductPage(Page):
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ParentalManyToManyField('product.ProductTag', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('product_name'),
        FieldPanel('product_code'),
        FieldPanel('image'),
        FieldPanel('tags', widget=forms.CheckboxSelectMultiple),
    ]

class ProductIndexPage(RoutablePageMixin, Page):
    subpage_types = ['product.ProductPage']

    body = StreamField([
        ("hero_section_2", HeroSectionBlock()),
        
    ], use_json_field=True ,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    @route(r'^$')
    @route(r'^page/(?P<page>\d+)/$')
    def all_products(self, request, page=1):
        return self.render(request, page=int(page))

    @route(r'^tag/(?P<tag_slug>[-\w]+)/$')
    @route(r'^tag/(?P<tag_slug>[-\w]+)/page/(?P<page>\d+)/$')
    def products_by_tag(self, request, tag_slug=None, page=1):
        return self.render(request, tag_slug=tag_slug, page=int(page))

    @route(r'^(?P<category_slug>[-\w]+)/$')
    @route(r'^(?P<category_slug>[-\w]+)/page/(?P<page>\d+)/$')
    def products_by_category(self, request, category_slug=None, page=1):
        return self.render(request, category_slug=category_slug, page=int(page))

    
    @route(r'^(?P<category_slug>[-\w]+)/tag/(?P<tag_slug>[-\w]+)/$')
    @route(r'^(?P<category_slug>[-\w]+)/tag/(?P<tag_slug>[-\w]+)/page/(?P<page>\d+)/$')
    def products_by_category_and_tag(self, request, category_slug, tag_slug, page=1):
        return self.render(request, category_slug=category_slug, tag_slug=tag_slug, page=int(page))

    def get_context(self, request, category_slug=None, tag_slug=None, page=1, **kwargs):
        context = super().get_context(request)

        products = ProductPage.objects.live().descendant_of(self)

        if tag_slug:
            tag = get_object_or_404(ProductTag, slug=tag_slug)
            products = products.filter(tags=tag)
            context['current_tag'] = tag

        if category_slug:
            category = get_object_or_404(ProductCategory, slug=category_slug)
            products = products.filter(category=category)
            context['current_category'] = category

        paginator = Paginator(products, 8)
        try:
            paginated_products = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            paginated_products = paginator.page(1)

        context.update({
            'products': paginated_products,
            'categories': ProductCategory.objects.all(),
            'tags': ProductTag.objects.all(),
            'paginator': paginator,
        })

        return context