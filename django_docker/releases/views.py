from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Release
from django.http import FileResponse,Http404

@login_required
def releases(request):
    releases = Release.objects.all()
    return render(request, 'releases/releases.html', {'releases': releases})
@login_required
def upload_release(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file.name.endswith('.bin'):
            release = Release(file=file)
            release.save()
            return redirect('releases:releases')
    # Handle invalid file or other errors
    return redirect('releases:releases')

@login_required
def download_release(request, filename):
    try:
        release = Release.objects.get(file__icontains=filename, file__endswith='.bin')
    except Release.DoesNotExist:
        raise Http404("Release not found")

    file_path = release.file.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)