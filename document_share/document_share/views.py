from django.shortcuts import render
from share.models import Document


def home(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    documents = Document.objects.filter(users__username=username)
    my_docs = Document.objects.filter(owner=username)

    return render(request, 'home.html', {'username': username, 'documents': documents, 'my_docs': my_docs})
