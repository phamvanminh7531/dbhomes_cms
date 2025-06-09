from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from streams.blocks import TechnologyBlock, PartnerBlock
from streams.blocks import EcosystemBlock, AboutUsBlock, ServicesBlock, HeroSectionBlock


class HomePage(Page):
    body = StreamField([
        ("hero_section_2", HeroSectionBlock()),
        ("technology_section", TechnologyBlock()),
        ("partner_section", PartnerBlock()),
        ("ecosystem_section", EcosystemBlock()),
        ("about_us_section", AboutUsBlock()),
        ("services_section", ServicesBlock()),

        
    ], use_json_field=True ,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Trang chủ"