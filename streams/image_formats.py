# image_formats.py
from django.utils.html import format_html
from wagtail.images.formats import Format, register_image_format

class CaptionedImageFormat(Format):
    def image_to_html(self, image, alt_text, extra_attributes=None):
        # Get the default image HTML
        default_html = super().image_to_html(image, alt_text, extra_attributes)
        
        # Wrap in figure with figcaption
        return format_html(
            '<figure class="image">{}<figcaption>{}</figcaption></figure>',
            default_html,
            alt_text
        )

# Register the format
register_image_format(
    CaptionedImageFormat(
        'captioned_fullwidth', 
        'Full width captioned', 
        'bodytext-image', 
        'width-750'
    )
)