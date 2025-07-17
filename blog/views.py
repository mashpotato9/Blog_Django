from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Category, Blog, Comment
from .forms import BlogForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def detail(request, post_id):
    # Logic to retrieve the post by post_id
    return render(request, 'details.html')

@login_required(login_url='blogAuth:login')
@require_http_methods(["GET", "POST"])
def post_blog(request):
    # Logic to handle posting a blog
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'post_blog.html', context={'categories': categories})

    elif request.method == 'POST':
        # Handle form submission
        form = BlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category_id = form.cleaned_data['category']
            # Logic to save the blog post
            Blog.objects.create(
                title=title,
                content=content,
                category_id=category_id,
                author=request.user
            )
            return JsonResponse({'status': 201, 'message': 'Blog posted successfully'})
        else:
            print(form.errors)
            return JsonResponse({'status': 400, 'errors': form.errors})