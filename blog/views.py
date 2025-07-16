from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def detail(request, post_id):
    # Logic to retrieve the post by post_id
    return render(request, 'details.html')