from wagtailseo.models import SeoMixin
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from streams.blocks import TechnologyBlock, PartnerBlock, CustomerFeedBackBlock
from streams.blocks import EcosystemBlock, AboutUsBlock, ServicesBlock, HeroSectionBlock, HotProject, HotNews


class HomePage(SeoMixin, Page):
    promote_panels = SeoMixin.seo_panels
    body = StreamField([
        ("hero_section_2", HeroSectionBlock()),
        ("hot_project_section", HotProject()),
        ("technology_section", TechnologyBlock()),
        ("partner_section", PartnerBlock()),
        ("ecosystem_section", EcosystemBlock()),
        ("about_us_section", AboutUsBlock()),
        ("HotNews", HotNews()),
        ("customer_feedback_block", CustomerFeedBackBlock()),
        ("services_section", ServicesBlock()),
        

        
    ], use_json_field=True ,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Trang chủ"