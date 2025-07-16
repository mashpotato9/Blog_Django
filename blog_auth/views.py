from django.shortcuts import render
from django.http.response import JsonResponse
from django.core.mail import send_mail
from .models import Capture
import string, random

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def send_captcha(request):
    # Logic to send a captcha to the user
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'error': 'Email is required'}, status=400)

    # Send the captcha to the user's email
    random_string = ''.join(random.sample(string.digits, 4))
    Capture.objects.update_or_create(email=email, defaults={'code': random_string})
    send_mail(
        'Your Captcha Code',
        message=f'Your captcha code is: {random_string}',
        from_email=None,
        recipient_list=[email],
    )
    return JsonResponse({'success': 'Captcha sent successfully'}, status=200)