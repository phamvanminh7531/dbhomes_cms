from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from streams.blocks import ContactFeatureSectionBlock, HeroSectionBlock, AboutUsMissionBlock, CoreValuesBlock, PartnerBlock, QASectionBlock, TechnologyBlock, OfficeMapSectionBlock
from streams.blocks import ContactFormBlock
# Create your models here.
class ContactPage(Page):
    body = StreamField([
        ("hero_section_2", HeroSectionBlock()),
        ("about_us_section", AboutUsMissionBlock()),
        ("core_values_section", CoreValuesBlock()),
        ("technology_section", TechnologyBlock()),
        ("partner_section", PartnerBlock()),
        ("qa_section", QASectionBlock()),
        ("contact_block", ContactFormBlock()),
        ("office_map_section", OfficeMapSectionBlock()),
        ("contact_feature_section", ContactFeatureSectionBlock()),

        
    ], use_json_field=True ,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Trang Liên hệ"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12, null=False, blank=False)
    address = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"