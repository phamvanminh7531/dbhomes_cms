from wagtail import hooks
from .admin import contact_submission_viewset

@hooks.register('register_admin_viewset')
def register_contact_submission_viewset():
    return contact_submission_viewset
