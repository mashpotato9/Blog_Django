from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model, login
from .models import Capture
from .forms import SignupForm, LoginForm
import string, random, json

User = get_user_model()

@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            # .check_password is a method of User model to verify password
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect(reverse('blog:index'))  # Redirect to the blog index page after login
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password'})
        else:
            return render(request, 'login.html', {'form': form})
    # Fallback for any other request method
    return render(request, 'login.html')
        
@require_http_methods(["GET", "POST"])
def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():  # trigger clean_email and clean_captcha
            # If the form is valid, we can proceed to create the user
            # create the user
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('blogAuth:login')) # Redirect to login after successful signup
        else:
            # If the form is not valid, return the errors
            print("Form validation errors:", form.errors)
            return render(request, 'signup.html', {'form': form, 'errors': form.errors})
    
    # Fallback for any other request method
    return render(request, 'signup.html')
        
        
def send_captcha(request: HttpRequest) -> JsonResponse:
    # Logic to send a captcha to the user
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
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