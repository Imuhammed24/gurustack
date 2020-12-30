from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'html_title': 'Gurustack_Home',})
