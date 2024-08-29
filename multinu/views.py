from django.shortcuts import render

def index(request):
    return render(request, 'multinu/index.html')
