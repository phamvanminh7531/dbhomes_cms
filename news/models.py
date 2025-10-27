# Create your models here.
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from wagtail.snippets.models import register_snippet
from wagtail.models import Page
from wagtail.fields import StreamField
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.models import Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.fields import ParentalManyToManyField
from streams.blocks import HeadingBlock, ImageBlock, CustomTableBlock, PharagraphBlock, TwoImagesBlock, HeroSectionBlock
from django.utils.text import slugify
from django import forms
from unidecode import unidecode
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable
from wagtailseo.models import SeoMixin, SeoType
from django.core.exceptions import ValidationError
from wagtail.admin.widgets import SlugInput



class NewsPageForm(WagtailAdminPageForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].widget = SlugInput(formatters=[
                                                            # --- Chữ thường không dấu ---
                                                            [r"[àáạảãâầấậẩẫăằắặẳẵ]", "a"],
                                                            [r"[èéẹẻẽêềếệểễ]", "e"],
                                                            [r"[ìíịỉĩ]", "i"],
                                                            [r"[òóọỏõôồốộổỗơờớợởỡ]", "o"],
                                                            [r"[ùúụủũưừứựửữ]", "u"],
                                                            [r"[ỳýỵỷỹ]", "y"],
                                                            [r"đ", "d"],

                                                            # --- Chữ hoa không dấu ---
                                                            [r"[ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴ]", "A"],
                                                            [r"[ÈÉẸẺẼÊỀẾỆỂỄ]", "E"],
                                                            [r"[ÌÍỊỈĨ]", "I"],
                                                            [r"[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", "O"],
                                                            [r"[ÙÚỤỦŨƯỪỨỰỬỮ]", "U"],
                                                            [r"[ỲÝỴỶỸ]", "Y"],
                                                            [r"Đ", "D"],
                                                        ])

    def clean(self):
        cleaned_data = super().clean()
        related_posts = cleaned_data.get("related_posts")

        if related_posts and len(related_posts) != 3:
            self.add_error(
                'related_posts',
                "Chỉ được chọn tối đa 3 bài viết liên quan."
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

class NewsPage(SeoMixin, Page):
    base_form_class = NewsPageForm
    subpage_types = []

    # Indicate this is article-style content.
    seo_content_type = SeoType.ARTICLE
    promote_panels = SeoMixin.seo_panels

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
        help_text="Chọn tối đa 3 bài viết liên quan."
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
        snippet = MostViewedNewsList.objects.first()
        context['snippet'] = snippet
        if self.related_posts.exists():
            context["related_posts"] = self.related_posts.all()
        elif self.category:
            context["related_posts"] = NewsPage.objects.live().filter(
                category=self.category
            ).exclude(id=self.id)[:3]
        else:
            context["related_posts"] = NewsPage.objects.live().exclude(id=self.id)[:3]
        return context

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()

        # Tạo slug giống như trong save
        generated_slug = slugify(unidecode(self.title))

        # Kiểm tra slug đã tồn tại chưa, trừ chính nó (nếu đang sửa)
        existing_pages = NewsPage.objects.filter(slug=generated_slug).exclude(pk=self.pk)

        if existing_pages.exists():
            raise ValidationError({
                'title': "Tiêu đề này sau khi chuyển thành slug đã bị trùng. Vui lòng thêm salt cho tiêu đề."
            })
    
    
    class Meta:
        verbose_name = "Bài viết Tin Tức"
        verbose_name_plural = "Bài viết Tin Tức"



class NewsIndexPage(RoutablePageMixin, Page):
    subpage_types = []
    body = StreamField([
        ("hero_section_2", HeroSectionBlock()),
        
    ], use_json_field=True ,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    @route(r'^$')
    @route(r'^page/(?P<page>\d+)/$')
    def all_news(self, request,page=1):
        return self.render(request, page=int(page))
    
    @route(r'^(?P<category_slug>[-\w]+)/$')
    @route(r'^(?P<category_slug>[-\w]+)/page/(?P<page>\d+)/$')
    def products_by_category(self, request, category_slug=None, page=1):
        return self.render(request, category_slug=category_slug, page=int(page))
    
    def get_context(self, request, category_slug=None, page=1, **kwargs):
        context = super().get_context(request)

        news = NewsPage.objects.live().order_by('-date_created')

        if category_slug:
            category = get_object_or_404(NewsCategory, slug=category_slug)
            news = news.filter(category = category)
            context['current_category'] = category
        
        paginator = Paginator(news, 9)

        try:
            paginated_news = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            paginated_news = paginator.page(1)

        context.update({
            'news_list': paginated_news,
            'categories': NewsCategory.objects.all(),
            'paginator': paginator,
        })

        return context

@register_snippet
class MostViewedNewsList(ClusterableModel):
    title = models.CharField(max_length=255, default="Danh sách bài viết xem nhiều nhất", editable=False)

    panels = [
        InlinePanel("items", label="Dự án được chọn"),
    ]

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Dự án nổi bật"
        verbose_name_plural = "Danh sách bài viết được xem nhiều nhất"

class MostViewedNewsItem(Orderable):
    parent = ParentalKey(MostViewedNewsList, on_delete=models.CASCADE, related_name="items")
    news = models.ForeignKey(NewsPage, on_delete=models.CASCADE)

    panels = [
        FieldPanel("news"),
    ]

    class Meta:
        verbose_name = "Bài viết được xem nhiều nhất"
        verbose_name_plural = "Danh sách bài viết được xem nhiều nhất"