from .models import Post

from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        save_post(request)
    
    return render(request, 'guestbook/index.html', {'here': Post.objects.all()})
    

def save_post(request):
    post = Post(name=request.POST.get('name'), message=request.POST.get('message'))
    post.save()
