# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import json
from .models import ContactSubmission
from django.core.mail import send_mail
from django.conf import settings
import threading



@require_http_methods(["POST"])
def contact_form_submit(request):
    """Handle contact form submission"""
    try:
        # Get form data
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        message = request.POST.get('message')

        print(name)
        
        # Validate required fields
        if not all([name, phone_number, address, message]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'All required fields must be filled.'})
            messages.error(request, 'All required fields must be filled.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        # Create submission
        submission = ContactSubmission.objects.create(
            name=name,
            phone_number=phone_number,
            address=address,
            message=message
        )
        # notify_admin_by_email(submission)
        threading.Thread(target=notify_admin_by_email, args=(submission,)).start()

        success_message = 'Cảm ơn bạn đã liên hệ, chúng tôi sẽ phản hồi sớm nhất.'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': success_message})

        # Nếu không phải AJAX, redirect như bình thường
        messages.success(request, success_message)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'An error occurred. Please try again.'})
        messages.error(request, 'An error occurred. Please try again.')
        return redirect(request.META.get('HTTP_REFERER', '/'))



def notify_admin_by_email(submission):
    subject = f"[Contact] Thông báo liên hệ từ {submission.name}"

    context = {
        'name': submission.name,
        'phone_number': submission.phone_number,
        'address': submission.address,
        'message': submission.message,
        'submitted_at': submission.submitted_at,
    }

    html_content = render_to_string('emails/contact_notification.html', context)
    text_content = f"""
Bạn có liên hệ mới từ {submission.name} ({submission.phone_number})
Địa chỉ: {submission.address}
Thời gian: {submission.submitted_at.strftime('%Y-%m-%d %H:%M')}

Nội dung:
{submission.message}
    """

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [email for _, email in settings.ADMINS],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()