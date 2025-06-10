from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from streams.blocks import HeroSectionBlock, AboutUsMissionBlock, CoreValuesBlock, PartnerBlock, ServicesBlock, TechnologyBlock, QASectionBlock, WorkflowSectionBlock
# Create your models here.
class ServicePage(Page):
    body = StreamField([
        ("hero_section_2", HeroSectionBlock()),
        ("about_us_section", AboutUsMissionBlock()),
        ("core_values_section", CoreValuesBlock()),
        ("technology_section", TechnologyBlock()),
        ("partner_section", PartnerBlock()),
        ("qa_section", QASectionBlock()),
        ("service_section", ServicesBlock()),
        ("workflow_section", WorkflowSectionBlock())


        
    ], use_json_field=True ,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ] 

    class Meta:
        verbose_name = "Trang Dịch vụ"