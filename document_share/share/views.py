from django.shortcuts import render, redirect
from datetime import datetime
from .forms import DocumentForm


def simple_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user.username
            document.upload_date = datetime.now()
            document.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'download.html', {'form': form})

# Create your views here.
