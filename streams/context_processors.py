from .models import FooterSettings, Menu, ContactButton

def footer_settings(request):
    """
    Context processor để thêm footer settings vào tất cả templates
    """
    try:
        footer_settings = FooterSettings.objects.select_related(
            'capacity_profile',
            'menu_items'
        ).prefetch_related(
            'office_addresses',
            'social_links',
            'social_links__logo_image',
            'menu_items__menu_items'
        ).first()
        
        return {
            'footer_settings': footer_settings
        }
    except FooterSettings.DoesNotExist:
        return {
            'footer_settings': None
        }

def contact_buttons(request):
    return {
        'contact_buttons': ContactButton.objects.all()
    }

def navbar(request):
    """
    Trả về menu đầu tiên (navbar chính) vào context của tất cả template.
    """
    menu = Menu.objects.first()
    return {
        "navbar_menu": menu,
    }
