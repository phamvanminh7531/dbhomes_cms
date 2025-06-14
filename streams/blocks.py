
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

# blocks.py - Kiểm tra import đầy đủ
from wagtail import blocks
from wagtail.blocks import URLBlock, StructBlock, RichTextBlock, ChoiceBlock, PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock  # Import này quan trọng
from wagtail.snippets.blocks import SnippetChooserBlock
from .models import Menu, HeroSection  # Import Menu model
from wagtail.contrib.table_block.blocks import TableBlock



# "-------------------------------------------------------------------------------------------------------------------"

# class NavBarBlock(blocks.StructBlock):
#     """Navbar Block với logo và menu items"""
#     logo_image = ImageChooserBlock(required=False, help_text="Logo (hình ảnh)")
#     logo_alt = blocks.CharBlock(required=False, help_text="Alt text cho logo", max_length=255)
#     # menu_items = blocks.ListBlock(NavItemBlock())
#     menu_items = SnippetChooserBlock(Menu, required=True, help_text="Chọn menu từ danh sách đã tạo")

#     class Meta:
#         template = "streams/navbar_block.html"
#         icon = "site"
#         label = "Navbar có logo"
# "-----------------------------------------BASE BLOCK-----------------------------------------------------"
class CTAButtonBlock(blocks.StructBlock):
    """CTA button Block"""
    label = blocks.CharBlock(required=True, help_text="Nhãn nút")
    url = blocks.CharBlock(required=False, null = True, blank=True ,help_text="Đường dẫn khi bấm")
    page = PageChooserBlock(required=False, null = True, blank=True, help_text="Trang liên kết")

    class Meta:
        icon = "plus"
        label = "CTA Button"

class FeatureItemBlock(blocks.StructBlock):
    "Block cho các số liệu nổi bật"
    number = blocks.CharBlock(required=True, help_text="Số liệu nổi bật (VD: 100+)")
    description = blocks.CharBlock(required=True, help_text="Mô tả ngắn về số liệu nổi bật (VD: Dự án đã hoàn thành)")

    class Meta:
        icon = "star"
        label = "Số liệu nổi bật"

class Background(blocks.StructBlock):
    """ Block cho hình nền """
    image = ImageChooserBlock(required=True, help_text="Hình ảnh nền (kích thước tối thiểu 1920x1080px)")
    alt_text = blocks.CharBlock(required=False, help_text="Alt text cho hình nền")

    class Meta:
        icon =  'image'
        label = 'Hình nền'

class TitleContentBlock(blocks.StructBlock):
    """Block cho tiêu đề và nội dung"""
    title = blocks.CharBlock(required=True, help_text="Tiêu đề cho nhóm nội dung")
    content = RichTextBlock(
        required=True,
        help_text= "Nội dung",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code" ]  # Các tính năng có thể tùy chỉnh,
    )

    class Meta:
        icon = "title"
        label = "Tiêu đề và Nội dung"

class TitileContentIconBlock(blocks.StructBlock):
    """Block cho tiêu đề, nội dung và icon"""
    title = blocks.CharBlock(required=True, help_text="Tiêu đề cho nhóm nội dung")
    content = RichTextBlock(
        required=True,
        help_text= "Nội dung",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code" ]  # Các tính năng có thể tùy chỉnh,
    )
    icon = ImageChooserBlock(required=True, help_text="Hình ảnh biểu tượng (kích thước tối ưu 100x100px v.v)")

    class Meta:
        icon = "icon"
        label = "Tiêu đề, Nội dung và Icon"

class QAItemBlock(blocks.StructBlock):
    """Block cho câu hỏi và câu trả lời"""
    question = blocks.CharBlock(required=True, help_text="Câu hỏi")
    answer = RichTextBlock(
        required=True,
        help_text="Câu trả lời",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code" ]  # Các tính năng có thể tùy chỉnh,
    )

    class Meta:
        icon = "help"
        label = "Câu hỏi và Câu trả lời"

# "-------------------------------------------------------------------------------------------------------------------"
# class Hero1SectionBlock(blocks.StructBlock):
#     """Hero Section Block với layout cố định"""
#     title = blocks.CharBlock(required=True, help_text="Tiêu đề chính hiển thị lớn")
#     background_images = blocks.ListBlock(
#         ImageChooserBlock(required=True),
#         help_text="Danh sách ảnh nền sẽ được hiển thị trong swiper"
#     )
#     buttons = blocks.ListBlock(CTAButtonBlock(), min_num=0, max_num=3)

#     class Meta:
#         template = "streams/hero_cta_slider_section_block.html"
#         icon = "image"
#         label = "Hero 1 Section"

# "-------------------------------------------------------------------------------------------------------------------"
class HotNews(blocks.StructBlock):
    news_list = blocks.ListBlock(
        PageChooserBlock(required=True, min_num = 3, max_num = 3, target_model='news.NewsPage'),
        help_text="Chọn 3 bài tin tức hiển thị"
    )

    class Meta:
        template = "streams/hot_news_block.html"
        icon = "folder-open-inverse"
        label = "Tin tức"




# "-------------------------------------------------------------------------------------------------------------------"
class HotProject(blocks.StructBlock):
    content = TitleContentBlock(required = True, help_text="Nội dung tiêu đề")
    projects = blocks.ListBlock(
        PageChooserBlock(required=True, target_model='project.ProjectPage'),
        help_text="Chọn các dự án nổi bật"
    )

    class Meta:
        template = "streams/featured_projects.html"
        icon = "folder-open-inverse"
        label = "Dự án nổi bật"

# "-------------------------------------------------------------------------------------------------------------------"

class HeroSectionBlock(blocks.StructBlock):
    hero_section_data = SnippetChooserBlock(HeroSection)
    layout = ChoiceBlock(choices=[
        ('hero_cta_slider_section_block', 'Hero section với CTA và slider'),
        ('hero_title_section_block', 'Hero section với tiêu đề)'),
        ('hero_empty_section_block', 'Hero section trống'),
    ], default='hero_empty_section_block')
    
    class Meta:
        template = "streams/hero_section_router.html"
        icon = "placeholder"
        label = "Hero section block"

# "-------------------------------------------------------------------------------------------------------------------"

class TechnologyBlock(blocks.StructBlock):
    """Technology Section Block với layout cố định"""
    
    # Block 1 - Text Left, Image Right
    block1_title_highlight = blocks.CharBlock(
        required=True,
        help_text="Phần highlight của title (VD: DB.Verse)",
        max_length=50,
        default="DB.Verse"
    )
    block1_title_main = blocks.CharBlock(
        required=True,
        help_text="Phần chính của title",
        max_length=200,
        default="Theo dõi dự án trong lòng bàn tay"
    )
    block1_paragraph1 = RichTextBlock(
        required=True,
        help_text="Đoạn văn đầu tiên",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code" ]  # Các tính năng có thể tùy chỉnh,
    )
    block1_image = ImageChooserBlock(
        required=True,
        help_text="Hình ảnh cho block 1 (phone mockup)"
    )
    
    # App Store buttons URLs
    appstore_url = blocks.URLBlock(
        required=False,
        help_text="Link App Store",
        default="https://apps.apple.com"
    )
    chplay_url = blocks.URLBlock(
        required=False,
        help_text="Link Google Play",
        default="https://play.google.com"
    )
    
    # Block 2 - Image Left, Text Right
    block2_title_highlight = blocks.CharBlock(
        required=True,
        help_text="Phần highlight của title block 2",
        max_length=50,
        default="DB.Verse"
    )
    block2_title_main = blocks.CharBlock(
        required=True,
        help_text="Phần chính của title block 2",
        max_length=200,
        default="Theo dõi dự án trong lòng bàn tay"
    )
    block2_paragraph = blocks.RichTextBlock(
        required=True,
        help_text="Đoạn văn thứ hai", 
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code" ]  # Các tính năng có thể tùy chỉnh,
    )
    block2_image = ImageChooserBlock(
        required=True,
        help_text="Hình ảnh cho block 2 (user holding phone)"
    )
    
    class Meta:
        template = "streams/technology_block.html"
        icon = "code"
        label = "Technology Section"


# "-------------------------------------------------------------------------------------------------------------------"

class MediaBlock(StructBlock):
    """Chọn video hoặc nhập link video"""
    video_file = DocumentChooserBlock(required=False, help_text="Tải lên video (.mp4, .mov)")
    video_url = URLBlock(required=False, help_text="Hoặc nhập link video YouTube/Vimeo")

    class Meta:
        icon = "media"
        label = "Video hoặc Link"

class PartnerBrandItemBlock(blocks.StructBlock):
    """Partner Brand Block cho các thương hiệu đối tác"""
    image = ImageChooserBlock(required=True, help_text="Hình ảnh logo thương hiệu")
    link = blocks.URLBlock(required=True, help_text="Đường dẫn đến trang của thương hiệu")

    class Meta:
        icon = "site"
        label = "Partner Brand Item"

class PartnerBlock(blocks.StructBlock):
    """Partner Section Block với danh sách các thương hiệu đối tác"""
    brands = blocks.ListBlock(PartnerBrandItemBlock(), min_num=1, max_num=7)
    main_media = MediaBlock(required=True, help_text="Ảnh hoặc video chính")

    class Meta:
        template = "streams/partner_block.html"
        icon = "group"
        label = "Partner Section"


# "-------------------------------------------------------------------------------------------------------------------"

class EcosystemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Tiêu đề của phần giới thiệu hệ sinh thái")
    description = RichTextBlock(
        required=True,
        help_text="Mô tả ngắn về hệ sinh thái",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )

    class Meta:
        template = "streams/ecosystem_block.html"
        icon = "group"
        label = "Ecosystem Section"

# "-------------------------------------------------------------------------------------------------------------------"

class AddressBlock(blocks.StructBlock):
    """"Block địa chỉ các văn phòng"""
    title = blocks.CharBlock(required=True, help_text="Tên văn phòng")
    address = blocks.CharBlock(required=True, help_text="Địa chỉ văn phòng")

    class Meta:
        icon =  'home'
        label = 'Địa chỉ văn phòng'

class FooterFollowUsBlock(blocks.StructBlock):
    """ Block cho các icon mạng xã hội trong footer """
    logo_image = ImageChooserBlock(required=True, help_text="Logo mạng xã hội (hình ảnh kích thước 50x50px)")
    logo_alt = blocks.CharBlock(required=True, help_text="Alt text cho icon mạng xã hội", max_length=255)
    link = blocks.URLBlock(required=True, help_text="Đường dẫn đến mạng xã hội")

    class Meta:
        icon =  'link'
        label = 'Đường dẫn mạng xã hội'

class FooterBlock(blocks.StructBlock):
    """"Block Footer"""
    capacity_profile = DocumentChooserBlock(required=False, help_text="Tải lên hồ sơ năng lực (.pdf)")
    menu_items = SnippetChooserBlock(Menu, required=True, help_text="Chọn menu từ danh sách đã tạo")
    follow_us = blocks.ListBlock(FooterFollowUsBlock(), min_num=1, max_num=6, help_text="Danh sách các mạng xã hội")
    addresses = blocks.ListBlock(AddressBlock(), min_num=1, max_num=3, help_text="Danh sách các địa chỉ văn phòng")
    contact = RichTextBlock(
        required=True,
        help_text="Thông tin liên hệ",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )

    class Meta:
        template = "streams/footer_block.html"
        icon = "site"
        label = "Footer Block với menu và mạng xã hội"

# "-------------------------------------------------------------------------------------------------------------------"
class AboutUsBlock(blocks.StructBlock):
    content = RichTextBlock(
        required=True,
        help_text="Nội dung giới thiệu về công ty",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )
    buttons = blocks.ListBlock(CTAButtonBlock(), min_num=0, max_num=2, help_text="Danh sách các nút CTA")
    feature_items = blocks.ListBlock(FeatureItemBlock(), min_num=1, max_num=4, help_text="Danh sách các số liệu nổi bật")
    background = Background(required=False, help_text="Thiết lập hình nền cho section này")

    class Meta:
        template = "streams/about_us_block.html"
        icon = "user"
        label = "Giới thiệu"

# "-------------------------------------------------------------------------------------------------------------------"
class ServiceItem(blocks.StructBlock):
    """Block cho các dịch vụ công ty"""
    title = blocks.CharBlock(required=True, help_text="Tiêu đề dịch vụ")
    description = RichTextBlock(
        required=True,
        help_text="Nội dung mô tả dịch vụ",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )
    icon = ImageChooserBlock(required=True, help_text="Hình ảnh biểu tượng dịch vụ (kích thước tối ưu 100x100px)")
    hover_image = ImageChooserBlock(required=True, help_text="Hình ảnh backgound khi hover")

    class Meta:
        icon = "cog"
        label = "Dịch vụ công ty"

class ServicesBlock(blocks.StructBlock):
    """Block cho phần dịch vụ của công ty"""
    title = blocks.TextBlock(required=True, help_text="Tiêu đề của phần dịch vụ")
    description = RichTextBlock(
        required=True,
        help_text="Mô tả ngắn về phần dịch vụ",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )
    services = blocks.ListBlock(ServiceItem(), min_num=3, max_num=3, help_text="Danh sách các dịch vụ")

    class Meta:
        template = "streams/services_block.html"
        icon = "cog"
        label = "Dịch vụ"

# "-------------------------------------------------------------------------------------------------------------------"
class AboutUsBlock2(blocks.StructBlock):

    content = RichTextBlock(
        required=True,
        help_text="Nội dung giới thiệu về công ty",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )

    background = Background(required=False, help_text="Thiết lập hình nền cho section này")

    class Meta:
        template = "streams/about_us_2_block.html"
        icon = "user"
        label = "Giới thiệu"
# "-------------------------------------------------------------------------------------------------------------------"
class AboutUsMissionBlock(blocks.StructBlock):
    feature_items = blocks.ListBlock(FeatureItemBlock(), min_num=1, max_num=4, help_text="Danh sách các số liệu nổi bật")
    contents = blocks.ListBlock(TitleContentBlock(), min_num=1, max_num=3, help_text="Danh sách các tiêu đề và nội dung")
    image = ImageChooserBlock(required=True, help_text="Hình ảnh minh hoạ cho sứ mệnh")

    class Meta:
        template = "streams/about_us_mission_block.html"
        icon = "user"
        label = "Sứ mệnh và tầm nhìn"

# "-------------------------------------------------------------------------------------------------------------------"
class QASectionBlock(blocks.StructBlock):
    """Block section các câu hỏi thường gặp"""
    image = ImageChooserBlock(required=True, help_text="Hình ảnh trang trí")
    faq_items = blocks.ListBlock(QAItemBlock(), min_num=1, max_num=5, help_text="Danh sách các câu hỏi và câu trả lời")

    class Meta:
        template = "streams/qa_section_block.html"
        icon = "help"
        label = "Câu hỏi thường gặp (FAQ)"

# "-------------------------------------------------------------------------------------------------------------------"
class CoreValuesBlock(blocks.StructBlock):
    """ Block cho các giá trị cốt lỗi của công ty """
    block1_title_main = blocks.CharBlock(
        required=True,
        help_text="Phần chính của title",
        max_length=200,
        default="Theo dõi dự án trong lòng bàn tay"
    )
    block1_title_highlight = blocks.CharBlock(
        required=True,
        help_text="Phần highlight của title sẽ có màu khác",
        max_length=50,
        default="DB.Verse"
    )
    core_items = blocks.ListBlock(TitileContentIconBlock(), min_num=3, max_num=6, help_text="Danh sách các giá trị cốt lõi")

    class Meta:
        template = "streams/core_value_block.html"
        icon = "cog"
        label = "Giá trị cốt lõi"

# "-------------------------------------------------------------------------------------------------------------------"
class ContactFeatureSectionBlock(blocks.StructBlock):
    feature_items = blocks.ListBlock(TitileContentIconBlock(), min_num=3, max_num=3, help_text="Danh sách các feature")

    class Meta:
        template = "streams/contact_feature_block.html"
        icon = "cog"
        label = "Các tính năng nổi bật trang Contact"

# "-------------------------------------------------------------------------------------------------------------------"
class WorkflowSectionBlock(blocks.StructBlock):
    """ Block giới thiệu quy trình làm việc công ty"""
    title = TitleContentBlock(required=True, help_text="Tiêu đề cho phần quy trình làm việc")
    workflow_items = blocks.ListBlock(TitleContentBlock(), min_num=8, max_num=8, help_text="Các bước quy trình làm việc")

    class Meta:
        template = "streams/workflow_block.html"
        icon = "list-ol"
        label = "Block giới thiệu quy trình làm việc công ty"


# "-------------------------------------------------------------------------------------------------------------------"
class OfficeMapItemBlock(blocks.StructBlock):
    """Block cho các văn phòng công ty"""
    title = blocks.CharBlock(required=True, help_text="Tên văn phòng")
    address = blocks.CharBlock(required=True, help_text="Địa chỉ văn phòng")
    map_link = blocks.URLBlock(required=True, help_text="Link đến bản đồ (Google Maps)")

    class Meta:
        icon = "map"
        label = "Văn phòng công ty"

class OfficeMapSectionBlock(blocks.StructBlock):
    """Block cho phần bản đồ văn phòng công ty"""

    offices = blocks.ListBlock(OfficeMapItemBlock(), min_num=1, max_num=2, help_text="Danh sách các văn phòng công ty")

    class Meta:
        template = "streams/office_map_section_block.html"
        icon = "map"
        label = "Bản đồ văn phòng"
# "-------------------------------------------------------------------------------------------------------------------"
class FactoryBlock(blocks.StructBlock):
    """Block giới thiệu nhà máy"""
    image = ImageChooserBlock(required=True, help_text="Hình ảnh nhà máy")
    title = TitleContentBlock(required=True, help_text="Tiêu đề cho phần giới thiệu nhà máy")
    button = CTAButtonBlock(required=True, help_text="Nút CTA cho phần giới thiệu nhà máy")

    class Meta:
        template = "streams/factory_block.html"
        icon = "factory"
        label = "Giới thiệu nhà máy"

# "-------------------------------------------------------------------------------------------------------------------"
class WeAreDbhomesBlock(blocks.StructBlock):
    """Block giới thiệu về DBHomes"""
    image = ImageChooserBlock(required=True, help_text="Hình ảnh background")
    content = RichTextBlock(
        required=True,
        help_text="Nội dung giới thiệu về DBHomes",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )

    class Meta:
        template = "streams/we_are_dbhomes_block.html"
        icon = "factory"
        label = "We are DBHomes block"

# "-------------------------------------------------------------------------------------------------------------------"

class CustomerFeedback(blocks.StructBlock):
    customer_avatar = ImageChooserBlock(required=True, help_text="Hình ảnh avatar khách hàng")
    customer_name = blocks.CharBlock(required=True, help_text="Tên khách hàng")
    customer_project = blocks.CharBlock(required=True, help_text="Tên dự án")
    customer_feedback = RichTextBlock(
        required=True,
        help_text="Feedback của khách hàng",
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )
    class Meta:
        icon = "group"
        label = "Thông tin feedback của khách hàng"

class CustomerFeedBackBlock(blocks.StructBlock):
    feedbacks = blocks.ListBlock(CustomerFeedback(), min_num=1, max_num=10, help_text="Danh sách các feedback")

    class Meta:
        template = "streams/customer_feedback_block.html"
        icon = "factory"
        label = "Block hiển thị danh sách feedback của khách hàng"



# "-------------------------------------------------------------------------------------------------------------------"

class ContactFormBlock(blocks.StructBlock):
    """Block contact form"""
    image = ImageChooserBlock(required=True, help_text="Hình ảnh nhà máy")

    class Meta:
        template = "streams/contact_form_2_block.html"
        icon = "form"
        label = "Contact form"

# "-------------------------------------------------------------------------------------------------------------------"
class ProjectCategoryItems(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Tên danh mục")
    image = ImageChooserBlock(required=True, help_text="Hình ảnh đại diện cho danh mục dự án")
    link = blocks.CharBlock(required=True, help_text="Slug dẫn tới danh sách dự án vs: /du-an/quy-mo-can-ho-2pn/")
    
    
    class Meta:
        icon = "form"
        label = "Item danh mục project"

class ProjectHomePageBlock(blocks.StructBlock):
    title = TitleContentBlock(required=True, help_text="Tiêu đề cho phần giới thiệu danh mục project")
    items = blocks.ListBlock(ProjectCategoryItems(), min_num=3, max_num=3, help_text="Danh sách các Danh mục dự án")

    class Meta:
        template = "streams/project_category_block.html"
        icon = "form"
        label = "Block giới thiệu danh mục dự án"


# "-------------------------------------------BLOCK FOR CONTENT POST------------------------------------------------------"

# "-------------------------------------------BLOCK FOR CONTENT POST------------------------------------------------------"

# "-------------------------------------------BLOCK FOR CONTENT POST------------------------------------------------------"

# "-------------------------------------------BLOCK FOR CONTENT POST------------------------------------------------------"
class CustomTableBlock(TableBlock):
    class Meta:
        template = "streams/table_block.html"
        icon = "table"
        label = "Bảng tuỳ chỉnh"
        
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        
        # Debug: In ra để kiểm tra
        print(f"TableBlock value: {value}")
        print(f"TableBlock type: {type(value)}")
        
        return context
        

class HeadingBlock(blocks.StructBlock):
    """"Block cho tiêu đề"""
    heading_text = blocks.CharBlock(required=True)

    class Meta:
        template = "streams/heading_block.html"
        icon = "title"
        label = "Tiêu đề"

class ImageBlock(blocks.StructBlock):
    """Single Image Block"""
    image = ImageChooserBlock(required=True, help_text="Chọn hình ảnh")
    caption = blocks.CharBlock(required=False, help_text="Chú thích cho hình ảnh", max_length=255)
    
    class Meta:
        template = "streams/single_image_block.html"
        icon = "image"
        label = "Hình ảnh đơn"

class TwoImagesBlock(blocks.StructBlock):
    """ Two Images Block """
    image1 = ImageChooserBlock(required=True, help_text="Chọn hình ảnh đầu tiên")
    image2 = ImageChooserBlock(required=True, help_text="Chọn hình ảnh thứ hai")
    caption = blocks.CharBlock(required=False, help_text="Chú thích cho hình ảnh", max_length=255)

    class Meta:
        template = "streams/two_image_block.html"
        icon = "image"
        label = "Hình ảnh đôi"

class PharagraphBlock(blocks.StructBlock):
    """Paragraph Block"""
    text = RichTextBlock(
        required=True,
        features=["h2", "h3", "bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "blockquote", "superscript", "subscript", "strikethrough", "code"]
    )

    class Meta:
        template = "streams/paragraph_block.html"
        icon = "pilcrow"
        label = "Đoạn văn"