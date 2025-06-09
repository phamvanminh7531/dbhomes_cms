# Create your models here.
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.models import Page
from wagtail.fields import RichTextField
from modelcluster.models import ClusterableModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.fields import ParentalManyToManyField
from django.core.exceptions import ValidationError
from streams.blocks import HeadingBlock, ImageBlock, CustomTableBlock, PharagraphBlock, TwoImagesBlock, HeroSectionBlock
from django.utils.text import slugify
from django import forms

from wagtail.admin.forms import WagtailAdminPageForm

class NewsPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()
        related_posts = cleaned_data.get("related_posts")

        if related_posts and len(related_posts) > 5:
            self.add_error(
                'related_posts',
                "Chỉ được chọn tối đa 5 bài viết liên quan."
            )

        return cleaned_data


@register_snippet
class NewsCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "NewsCategory"
        verbose_name_plural = "NewsCategories"

class NewsPage(Page):
    base_form_class = NewsPageForm
    subpage_types = []
    hero_section = StreamField([
        ('hero_section', HeroSectionBlock()),
        # Thêm các block khác nếu có
    ], blank=False, max_num=1, use_json_field=True, )

    # Thông tin cơ bản
    category = models.ForeignKey(
        "news.NewsCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="news_pages"
    )

    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    related_posts = ParentalManyToManyField(
        'news.NewsPage',
        blank=True,
        related_name='related_to',
        verbose_name="Bài viết liên quan",
        help_text="Chọn tối đa 5 bài viết liên quan."
    )


    # Nội dung
    content = StreamField([
        
        ("heading", HeadingBlock()),
        ("paragraph", PharagraphBlock()),
        ("image", ImageBlock()),
        ("two_images", TwoImagesBlock()),
        ("table", CustomTableBlock()),
    ], use_json_field=True, blank=True)

    # Thông tin meta
    date_created = models.DateField("Ngày tạo", blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_section'),
        MultiFieldPanel([
            FieldPanel("category"),
            FieldPanel("date_created"),
        ], heading="Thông tin cơ bản"),
        MultiFieldPanel([
            FieldPanel("intro_image"),
        ], heading="Hình ảnh"),
        FieldPanel("content"),
        FieldPanel("related_posts", widget=forms.CheckboxSelectMultiple),
    ]    
   
    def get_context(self, request):
        context = super().get_context(request)
        if self.related_posts.exists():
            context["related_posts"] = self.related_posts.all()
        elif self.category:
            context["related_posts"] = NewsPage.objects.live().filter(
                category=self.category
            ).exclude(id=self.id)[:4]
        else:
            context["related_posts"] = NewsPage.objects.live().exclude(id=self.id)[:4]
        return context
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

class NewsIndexPage(Page, ClusterableModel):
    subpage_types = []
    intro = RichTextField(blank=True, help_text="Giới thiệu về trang tin tức")
    
    # Cài đặt hiển thị
    posts_per_page = models.IntegerField(
        default=12,
        help_text="Số bài viết hiển thị mỗi trang"
    )
    
    show_categories = models.BooleanField(
        default=True,
        help_text="Hiển thị filter theo danh mục"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel([
            FieldPanel("posts_per_page"),
            FieldPanel("show_categories"),
        ], heading="Cài đặt hiển thị"),
        
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        # Lấy tất cả bài viết con
        news_pages = NewsPage.objects.live().descendant_of(self)

        # Filter theo category
        category_slug = request.GET.get("category")
        if category_slug:
            try:
                category = NewsCategory.objects.get(slug=category_slug)
                news_pages = news_pages.filter(category=category)
                context["current_category"] = category
            except NewsCategory.DoesNotExist:
                pass

        # Pagination
        paginator = Paginator(news_pages, self.posts_per_page)
        page = request.GET.get('page')
        
        try:
            news_pages = paginator.page(page)
        except PageNotAnInteger:
            news_pages = paginator.page(1)
        except EmptyPage:
            news_pages = paginator.page(paginator.num_pages)

        context["news_pages"] = news_pages
        context["categories"] = NewsCategory.objects.all()
    
        
        # Thống kê
        context["total_posts"] = NewsPage.objects.live().descendant_of(self).count()
        context["categories_with_count"] = [
            {
                'category': cat,
                'count': NewsPage.objects.live().descendant_of(self).filter(category=cat).count()
            }
            for cat in NewsCategory.objects.all()
        ]
        
        return context
    
    class Meta:
        verbose_name = "News Index Page"