from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm, ImageSendForm
from django.core.files.storage import FileSystemStorage, default_storage
from PIL import Image, ExifTags
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden,FileResponse, HttpResponse, HttpResponseNotFound,JsonResponse
from django.contrib.staticfiles import finders
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64
import tempfile
from io import BytesIO
import json

image_accessed = False  # Flag to track image access

@require_GET
def get_all_images(request, username):
    media_path = Path(settings.MEDIA_ROOT) / username / 'uploaded'
    uploaded_image_data = {}

    for file_path in media_path.iterdir():
        if file_path.is_file():
            relative_url = file_path.relative_to(settings.MEDIA_ROOT)
            image_url = request.build_absolute_uri(settings.MEDIA_URL + str(relative_url))
            uploaded_image_data[file_path.name] = image_url

    return JsonResponse({'uploaded_images': uploaded_image_data})
@login_required
def serve_uploaded_images(request, username, image):
    image_path = Path(settings.MEDIA_ROOT) / username / 'uploaded' / image

    with open(image_path, 'rb') as img_file:
        return HttpResponse(img_file.read(), content_type='image/png')  # Adjust content_type based on your image type


@login_required
def send_image(request):
    if request.method == 'POST':
        form = ImageSendForm(user=request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            # Get the selected user from the form
            selected_user = form.cleaned_data['users']
            # Get the uploaded image from the form
            image_path = form.cleaned_data['image']

            with open(image_path, 'rb') as image_file:
            # Process the file as needed (e.g., save to another location)
            # In this example, it saves to the selected user's 'sent' folder
                Image_sent_path=Path(f'media/{selected_user.username}/sent/new.jpg')
                if Image_sent_path.is_file():
                    Path.unlink(Image_sent_path)

                fs = FileSystemStorage(location=f'media/{selected_user.username}/sent')
                filename = fs.save(Path("new.jpg").name, image_file)
                uploaded_file_path = fs.url(filename)

            return redirect('image_handling:crop', selected_user.username)
            # Redirect or render a success message
            #return render(request, 'accounts/success.html')
    else:
        form = ImageSendForm(user=request.user)

    return render(request, 'image_handling/send.html', {'form': form})

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded image
            image = form.cleaned_data['image']

            # Open the image using Pillow
            img = Image.open(image)

            # Check and apply orientation information
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif_data = dict(img._getexif().items())

                if exif_data[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif_data[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif_data[orientation] == 8:
                    img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # No EXIF data or orientation information
                pass

            # Convert the image to JPEG if it's a PNG
            if img.format == 'PNG':
                output_buffer = BytesIO()
                img = img.convert('RGB')
                img.save(output_buffer, format='JPEG')
                output_buffer.seek(0)
                image = ContentFile(output_buffer.getvalue(), name=image.name)

            # Create a temporary file to save the converted image
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image:
                image.seek(0)  # Reset the file pointer for reading
                temp_image.write(image.read())
                temp_image.close()

                # Create a pathlib Path object with the temporary file
                converted_file = Path(temp_image.name)

                # Save the image to the user's subfolder in the media directory
                img.save(f'media/{request.user.username}/uploaded/new.jpg', 'JPEG',optimize=True,quality=20)
                uploaded_file_path = f'media/{request.user.username}/uploaded/new.jpg'

                # Redirect to the profile page with a success message
                messages.success(request, 'Image saved successfully.')
                return redirect('accounts:profile')
        else:
            # Invalid form, handle appropriately
            pass
    else:
        form = ImageUploadForm()

    return render(request, 'image_handling/upload.html', {'form': form})

def latest_image(request, username):
    global image_accessed
    image_path = f'{settings.MEDIA_ROOT}/{username}/sent/resized_latest.jpg'
    if not image_accessed:
        try:
            image_file = open(image_path, 'rb')
            image_accessed = True  # Set the flag to True after the image is accessed
            return FileResponse(image_file, content_type='image/jpeg')
        except FileNotFoundError:
            return HttpResponse('Image not found', status=404)
    else:
        return HttpResponse('Image access restricted', status=404)  # Return forbidden status if image has already been accessed
def fetch_uncropped_image(request, username):
    image_path = f'{settings.MEDIA_ROOT}/{username}/sent/new.jpg'
    try:
        image_file = open(image_path, 'rb')
        return FileResponse(image_file, content_type='image/jpeg')
    except FileNotFoundError:
        return HttpResponse('Image not found', status=404)

@login_required
def display_image_cropping_page(request, selected_user):
    return render(request, 'image_handling/crop.html', {'selected_user': selected_user})

@csrf_exempt
def save_cropped_image(request, selected_user):
    if request.method == 'POST' and request.FILES.get('croppedImage'):
        global image_accessed
        cropped_image = request.FILES['croppedImage']
        image = Image.open(cropped_image)

        # Perform the cropping operation
        Image_resized_path=Path(f'media/{selected_user}/sent/resized_latest.jpg')
        if Image_resized_path.is_file():
            Path.unlink(Image_resized_path)
        # Resize the cropped image to 128x160
        resized_image = image.resize((128, 160))

        # Save the resized image to the media directory
        image_path = f'{settings.MEDIA_ROOT}/{selected_user}/sent/resized_latest.jpg'  # Replace with the desired path

        with BytesIO() as buffer:
            resized_image.save(buffer, format='JPEG')
            image_data = buffer.getvalue()

            with open(image_path, 'wb') as f:
                f.write(image_data)
            image_accessed = False
            messages.success(request,"Image cropped and sent successfully to "+selected_user)


        return JsonResponse({'message': 'Cropped and resized image saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def Delete_uploaded_image(request, username, image):
    image_path = Path(f'media/{username}/uploaded/{image}')
    if image_path.is_file():
        Path.unlink(image_path)

        return JsonResponse({'message': 'Cropped and resized image saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
