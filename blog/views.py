from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Blog, Comment
from .forms import BlogForm


# Create your views here.
def index(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'index.html', context={'blogs': blogs})


def detail(request, blog_id):
    # Logic to retrieve the post by blog_id
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog).order_by('-created_at')
    return render(request, 'details.html', context={'blog': blog, 'comments': comments})


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
            category_id = form.cleaned_data['category_id']
            # Logic to save the blog post
            blog = Blog.objects.create(
                title=title,
                content=content,
                category_id=category_id,
                author=request.user
            )
            return JsonResponse({'message': 'Blog posted successfully', 'blog_id': blog.pk}, status=201)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
        
    # fallback for any other request method
    return render(request, 'post_blog.html', context={'form': BlogForm(), 'categories': Category.objects.all()})

@require_POST
@login_required(login_url='blogAuth:login')
def post_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    Comment.objects.create(
        content=content,
        blog_id=blog_id,
        author=request.user
    )
    return redirect('blog:detail', blog_id=blog_id)

@require_GET
def search(request):
    # /search?q=keyword
    q = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by('-created_at')
    return render(request, 'index.html', context={'blogs': blogs})