from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def detail(request, post_id):
    # Logic to retrieve the post by post_id
    return render(request, 'details.html')

@login_required(login_url='blogAuth:login')
def post_blog(request):
    # Logic to handle posting a blog
    return render(request, 'post_blog.html')

