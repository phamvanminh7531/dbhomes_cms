from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.admin.filters import DateRangePickerWidget, WagtailFilterSet
from wagtail.admin.ui.tables import UpdatedAtColumn
from django.utils.html import format_html
from wagtail.admin.ui.tables import Column
import django_filters

from .models import ContactSubmission


class ContactSubmissionFilterSet(WagtailFilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        label="Submitted Date",  # ✅ Thêm label rõ ràng
        widget=DateRangePickerWidget
    )

    class Meta:
        model = ContactSubmission
        fields = ['created_at']


class ContactSubmissionViewSet(ModelViewSet):
    model = ContactSubmission
    icon = 'form'
    menu_label = 'Contact Submissions'
    menu_name = 'contact-submissions'
    menu_order = 200
    add_to_admin_menu = True

    list_display = ['name', 'phone_number', 'address', 'submitted_at', Column('message', label='Message Preview', accessor='get_message_preview')]
    list_filter = ['submitted_at']
    search_fields = ['name', 'phone_number', 'address', 'submitted_at', 'message']
    ordering = ['-submitted_at']

    exclude_form_views = ['add']  # ✅ Đúng cách để tắt tính năng tạo mới

    panels = [
        MultiFieldPanel([
            FieldPanel('name', read_only=True),
            FieldPanel('phone_number', read_only=True),
            FieldPanel('address', read_only=True),
        ], heading="Contact Information", classname="collapsed"),

        MultiFieldPanel([
            FieldPanel('message', read_only=True),
        ], heading="Message Details"),

        MultiFieldPanel([
            FieldPanel('submitted_at', read_only=True),
        ], heading="Submission Info", classname="collapsed"),
    ]

    filterset_class = ContactSubmissionFilterSet

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


    def get_message_preview(self, instance):
        if len(instance.message) > 100:
            return instance.message[:100] + '...'
        return instance.message


# Tạo viewset instance
contact_submission_viewset = ContactSubmissionViewSet('contact_contactsubmission')
