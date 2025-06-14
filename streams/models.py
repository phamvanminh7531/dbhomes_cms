# models.py
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable
from wagtail.images import get_image_model_string
from wagtail.documents import get_document_model_string
from wagtail.fields import RichTextField
from wagtail.admin.forms import WagtailAdminModelForm
from django.core.exceptions import ValidationError


@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=100)

    logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo (hình ảnh)"
    )

    logo_alt = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt text cho logo"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("logo_image"),
        FieldPanel("logo_alt"),
        InlinePanel("menu_items", label="Menu Items"),
    ]

    def __str__(self):
        return self.title


class MenuItem(Orderable):
    menu = ParentalKey(Menu, on_delete=models.CASCADE, related_name="menu_items")
    label = models.CharField(max_length=100)
    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Trang liên kết",
        help_text="Chọn trang liên kết đến nút nav bar item"
    )


    panels = [
        FieldPanel("label"),
        FieldPanel("page")
    ]

    def __str__(self):
        return self.label
    
# "-------------------------------------------------------------------------------------------------------------------"

class HeroSectionAdminForm(WagtailAdminModelForm):
    def clean(self):
        cleaned_data = super().clean()

        is_have_cta = cleaned_data.get("is_have_cta")
        is_multi_image = cleaned_data.get("is_multi_image")

        num_cta = 0
        num_images = 0

        # Kiểm tra mỗi formset có tồn tại cleaned_data chưa
        for name, formset in self.formsets.items():
            if not hasattr(formset, 'cleaned_data'):
                continue  # skip nếu chưa có cleaned_data (invalid hoặc chưa is_valid)

            if name == 'cta_buttons':
                num_cta = len([
                    form_data for form_data in formset.cleaned_data
                    if not form_data.get('DELETE', False)
                ])
            elif name == 'hero_images':
                num_images = len([
                    form_data for form_data in formset.cleaned_data
                    if not form_data.get('DELETE', False)
                ])
        # Kiểm tra điều kiện
        if is_have_cta == False and num_cta > 0:
            self.add_error('is_have_cta', ValidationError("Bạn đã thêm nút CTA nhưng không bật 'is_have_cta'."))

        if is_multi_image == False and num_images > 1:
            self.add_error('is_multi_image', ValidationError("Chỉ được thêm tối đa 2 hình ảnh khi không bật 'is_multi_image'."))

        return cleaned_data

@register_snippet
class HeroSection(ClusterableModel):
    base_form_class = HeroSectionAdminForm
    title = models.CharField(
        max_length=255,
        verbose_name="Tên Hero",
        help_text="Tên Hero"
    )
    display_text = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Văn bản hiển thị",
        help_text="Văn bản hiển thị trên phần Hero"
    )
    is_multi_image = models.BooleanField(
        default=False,
        verbose_name="Hiển thị nhiều hình ảnh",
        help_text="Chọn nếu phần Hero này sẽ hiển thị nhiều hình ảnh"
    )

    is_have_cta = models.BooleanField(
        default=False,
        verbose_name="Có nút CTA",
        help_text="Chọn nếu phần Hero này sẽ có nút CTA"
    )
    panels = [
        FieldPanel('title'),
        FieldPanel('display_text'),
        FieldPanel('is_multi_image'),
        FieldPanel('is_have_cta'),

        MultiFieldPanel([
            InlinePanel('hero_images', label="Hình ảnh Hero", min_num=1, max_num=5),
        ], heading="Hình ảnh Hero"),

        MultiFieldPanel([
            InlinePanel('cta_buttons', label="Nút CTA", min_num=0, max_num=3),
        ], heading="Nút CTA")
        
        ]

    def __str__(self):
        return self.title

class HeroImage(Orderable):
    hero_section = ParentalKey(
        HeroSection,
        related_name='hero_images',
        on_delete=models.CASCADE
    )
    
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        verbose_name="Hình ảnh",
        help_text="Hình ảnh hiển thị trong phần Hero"
    )
    
    alt_text = models.CharField(
        max_length=255,
        verbose_name="Alt text",
        help_text="Văn bản thay thế cho hình ảnh"
    )

    panels = [
        FieldPanel('image'),
        FieldPanel('alt_text'),
    ]

    def __str__(self):
        return f"{self.alt_text} - {self.image}"

class CTA_Button(Orderable):
    """
    Model cho nút CTA trong phần Hero
    """
    hero_section = ParentalKey(
        HeroSection,
        related_name='cta_buttons',
        on_delete=models.CASCADE
    )
    
    label = models.CharField(
        max_length=100,
        verbose_name="Nhãn nút",
        help_text="Nhãn hiển thị trên nút CTA"
    )
    
    link = models.URLField(
        verbose_name="Đường dẫn",
        help_text="Đường dẫn đến trang đích của nút CTA",
        null=True,
        blank=True,
    )

    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Trang liên kết",
        help_text="Chọn trang liên kết đến nút CTA"
    )

    panels = [
        FieldPanel('label'),
        FieldPanel('link'),
        FieldPanel('page'),
    ]

    def __str__(self):
        return self.label


# '-----------------------------------------------------------------------------------------------------------------------'

@register_snippet
class FooterSettings(ClusterableModel):
    """
    Footer snippet để quản lý toàn bộ nội dung footer
    """
    # Hồ sơ năng lực
    capacity_profile = models.ForeignKey(
        get_document_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Hồ sơ năng lực",
        help_text="Tải lên hồ sơ năng lực (.pdf)"
    )
    
    # Menu
    menu_items = models.ForeignKey(
        'streams.Menu',  # Thay 'your_app' bằng tên app chứa Menu model
        on_delete=models.CASCADE,
        verbose_name="Menu Footer",
        help_text="Chọn menu từ danh sách đã tạo"
    )
    
    # Thông tin liên hệ
    contact = RichTextField(
        verbose_name="Thông tin liên hệ",
        help_text="Thông tin liên hệ",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", 
                 "document-link", "image", "embed", "blockquote", 
                 "superscript", "subscript", "strikethrough", "code"]
    )

    panels = [
        FieldPanel('capacity_profile'),
        FieldPanel('menu_items'),
        FieldPanel('contact'),
        
        MultiFieldPanel([
            InlinePanel('social_links', label="Mạng xã hội", min_num=1, max_num=6),
        ], heading="Mạng xã hội"),
        
        MultiFieldPanel([
            InlinePanel('office_addresses', label="Địa chỉ văn phòng", min_num=1, max_num=3),
        ], heading="Địa chỉ văn phòng"),
    ]

    class Meta:
        verbose_name = "Footer Settings"
        verbose_name_plural = "Footer Settings"

    def __str__(self):
        return f"Footer Settings"


class FooterSocialLink(Orderable):
    """
    Model cho các icon mạng xã hội trong footer
    """
    footer = ParentalKey(
        FooterSettings,
        related_name='social_links',
        on_delete=models.CASCADE
    )
    
    logo_image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        verbose_name="Logo mạng xã hội",
        help_text="Logo mạng xã hội (hình ảnh kích thước 50x50px)"
    )
    
    logo_alt = models.CharField(
        max_length=255,
        verbose_name="Alt text cho icon",
        help_text="Alt text cho icon mạng xã hội"
    )
    
    link = models.URLField(
        verbose_name="Đường dẫn",
        help_text="Đường dẫn đến mạng xã hội"
    )

    panels = [
        FieldPanel('logo_image'),
        FieldPanel('logo_alt'),
        FieldPanel('link'),
    ]

    class Meta:
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"

    def __str__(self):
        return f"{self.logo_alt} - {self.link}"


class FooterOfficeAddress(Orderable):
    """
    Model cho địa chỉ các văn phòng
    """
    footer = ParentalKey(
        FooterSettings,
        related_name='office_addresses',
        on_delete=models.CASCADE
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name="Tên văn phòng",
        help_text="Tên văn phòng"
    )
    
    address = models.CharField(
        max_length=500,
        verbose_name="Địa chỉ văn phòng",
        help_text="Địa chỉ văn phòng"
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('address'),
    ]

    class Meta:
        verbose_name = "Office Address"
        verbose_name_plural = "Office Addresses"

    def __str__(self):
        return f"{self.title} - {self.address}"

