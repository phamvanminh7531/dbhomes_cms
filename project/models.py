# Create your models here.
from django.db import models
from django.shortcuts import get_object_or_404
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.models import Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.fields import ParentalManyToManyField
from streams.blocks import HeadingBlock, ImageBlock, CustomTableBlock, PharagraphBlock, TwoImagesBlock, HeroSectionBlock, ProjectHomePageBlock
from django.utils.text import slugify
from django import forms
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.http import Http404
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable
# Create your models here.

class ProjectPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()
        related_posts = cleaned_data.get("related_posts")

        if related_posts and len(related_posts) != 3:
            self.add_error(
                'related_posts',
                "Chọn 3 bài viết liên quan."
            )

        return cleaned_data

@register_snippet
class DesignStyle(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Danh sách phong cách thiết kế"
        verbose_name_plural = "Danh sách phong cách thiết kế"

@register_snippet
class ProjectScale(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Danh sách quy mô dự án"
        verbose_name_plural = "Danh sách quy mô dự án"

class ProjectHomePage(Page):
    body = StreamField([
        ("hero_section_2", HeroSectionBlock()),
        ("ProjectHomePageBlock", ProjectHomePageBlock()),

        
    ], use_json_field=True ,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Trang Dự án"
        verbose_name_plural = "Trang Dự án"

class ProjectPage(Page):
    base_form_class = ProjectPageForm
    subpage_types = []

    project_location = models.CharField(max_length=255, help_text="Vị trí (Tên chung cư, chủ đầu tư vv)")
    project_acreage = models.IntegerField(help_text="Diện tích")

    hero_section = StreamField([
        ('hero_section', HeroSectionBlock()),
        # Thêm các block khác nếu có
    ], blank=False, max_num=1, use_json_field=True, )

    # Thông tin cơ bản
    design_style = models.ForeignKey(
        "project.DesignStyle",
        on_delete=models.PROTECT,
        related_name="design_style"
    )
    project_scale = models.ForeignKey(
        "project.ProjectScale",
        on_delete=models.PROTECT,
        related_name="project_scale"
    )

    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
        related_name="+"
    )

    related_posts = ParentalManyToManyField(
        'project.ProjectPage',
        null=True,
        blank=True,
        related_name='related_to',
        verbose_name="Bài viết liên quan",
        help_text="Chọn 3 bài viết liên quan."
    )


    # Nội dung
    content = StreamField([    
        ("heading", HeadingBlock()),
        ("paragraph", PharagraphBlock()),
        ("image", ImageBlock()),
        ("two_images", TwoImagesBlock()),
        ("table", CustomTableBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_section'),
        MultiFieldPanel([
            FieldPanel("project_location"),
            FieldPanel("project_acreage"),
            FieldPanel("design_style"),
            FieldPanel("project_scale"),
        ], heading="Thông tin cơ bản"),
        
        MultiFieldPanel([
            
            FieldPanel("intro_image"),
        ], heading="Nội dung"),
        FieldPanel("content"),
        FieldPanel("related_posts", widget=forms.CheckboxSelectMultiple),
    ]
   
    def get_context(self, request):
        context = super().get_context(request)
        snippet = MostViewedProjectList.objects.first()
        context['snippet'] = snippet
        if self.related_posts.exists():
            context["related_posts"] = self.related_posts.all()
        elif self.design_style:
            context["related_posts"] = ProjectPage.objects.filter(
                design_style = self.design_style
            ).exclude(id=self.id)[:4]
        else:
            context["related_posts"] = ProjectPage.objects.live().exclude(id=self.id)[:4]
        return context
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Bài viết Dự Án"
        verbose_name_plural = "Bài viết Dự Án"

class ProjectIndexPage(RoutablePageMixin, Page):
    subpage_types = ["project.ProjectPage"]
    body = StreamField([
        ("hero_section_2", HeroSectionBlock()),
        
    ], use_json_field=True ,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    @route(r'^(?P<slug>[-\w]+)/$')
    @route(r'^(?P<slug>[-\w]+)/page/(?P<page>\d+)/$')
    def resolve_slug(self, request, slug, page=1):
        """
        Ưu tiên slug là ProjectPage → nếu không, tiếp tục lọc theo DesignStyle → nếu không, tiếp tục lọc theo ProjectScale
        """
        # 1. Kiểm tra ProjectPage
        try:
            child_page = ProjectPage.objects.live().descendant_of(self).get(slug=slug)
            return child_page.serve(request)
        except ProjectPage.DoesNotExist:
            pass

        # 2. Kiểm tra DesignStyle (nếu tồn tại)
        design_style = DesignStyle.objects.filter(slug=slug).first()
        if design_style:
            return self.projects_by_design_style(request, design_style_slug=slug, page=page)

        # 3. Kiểm tra ProjectScale (nếu tồn tại)
        project_scale = ProjectScale.objects.filter(slug=slug).first()
        if project_scale:
            return self.projects_by_project_scale(request, project_scale_slug=slug, page=page)

        # Nếu không khớp gì thì 404
        raise Http404("Không tìm thấy nội dung với slug này.")
            

    @route(r'^$')
    @route(r'^page/(?P<page>\d+)/$')
    def all_projects(self, request,page=1):
        return self.render(request, page=int(page))
    
    @route(r'^(?P<design_style_slug>[-\w]+)/$')
    @route(r'^(?P<design_style_slug>[-\w]+)/page/(?P<page>\d+)/$')
    def projects_by_design_style(self, request, design_style_slug=None, page=1):
        print("Stykle")
        return self.render(request, design_style_slug=design_style_slug, page=int(page))
    
    @route(r'^(?P<project_scale_slug>[-\w]+)/$')
    @route(r'^(?P<project_scale_slug>[-\w]+)/page/(?P<page>\d+)/$')
    def projects_by_project_scale(self, request, project_scale_slug=None, page=1):
        print("Quy mo")
        return self.render(request, project_scale_slug=project_scale_slug, page=int(page))
    
    @route(r'^(?P<design_style_slug>[-\w]+)/(?P<project_scale_slug>[-\w]+)/$')
    @route(r'^(?P<design_style_slug>[-\w]+)/(?P<project_scale_slug>[-\w]+)/page/(?P<page>\d+)/$')
    def products_by_design_style_and_project_scale(self, request, design_style_slug, project_scale_slug, page=1):
        return self.render(request, design_style_slug=design_style_slug, project_scale_slug=project_scale_slug, page=int(page))
    
    def get_context(self, request, design_style_slug=None, project_scale_slug=None, page=1, **kwargs):
        context = super().get_context(request)

        projects = ProjectPage.objects.live().descendant_of(self)

        if design_style_slug:
            design_style = get_object_or_404(DesignStyle, slug=design_style_slug)
            projects = projects.filter(design_style = design_style)
            context['current_design_style'] = design_style
        
        if project_scale_slug:
            project_scale = get_object_or_404(ProjectScale, slug=project_scale_slug)
            projects = projects.filter(project_scale = project_scale)
            context['current_project_scale'] = project_scale

        
        paginator = Paginator(projects, 9)

        try:
            paginated_projects = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            paginated_projects = paginator.page(1)

        context.update({
            'projects': paginated_projects,
            'desgin_styles': DesignStyle.objects.all(),
            'project_scales': ProjectScale.objects.all(),
            'paginator': paginator,
        })

        return context
    
    class Meta:
        verbose_name = "Trang Danh sách Dự án"
        verbose_name_plural = "Trang Danh sách Dự án"

@register_snippet
class MostViewedProjectList(ClusterableModel):
    title = models.CharField(max_length=255, default="Dự án được xem nhiều nhất", editable=False)

    panels = [
        InlinePanel("items", label="Dự án được chọn"),
    ]

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Dự án được xem nhiều nhất"
        verbose_name_plural = "Danh sách dự án được xem nhiều nhất"

class MostViewedProjectItem(Orderable):
    parent = ParentalKey(MostViewedProjectList, on_delete=models.CASCADE, related_name="items")
    project = models.ForeignKey(ProjectPage, on_delete=models.CASCADE)

    panels = [
        FieldPanel("project"),
    ]

    class Meta:
        verbose_name = "Dự án được xem nhiều nhất"
        verbose_name_plural = "Danh sách dự án được xem nhiều nhất"