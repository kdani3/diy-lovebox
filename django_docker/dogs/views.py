from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dogs(request):
    return render(request, 'dogs/dogs.html')
