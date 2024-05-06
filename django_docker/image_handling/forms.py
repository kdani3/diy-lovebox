from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings
from pathlib import Path

class ImageSendForm(forms.Form):
    User_model = get_user_model()
    users = forms.ModelChoiceField(queryset=User_model.objects.all())
    image = forms.ChoiceField(choices=[])
    
    def __init__(self, user, *args, **kwargs):
        super(ImageSendForm, self).__init__(*args, **kwargs)

        # Use the 'user' parameter directly
        self.user = user

        # Set the choices for the image field based on the user's uploaded images
        user_directory = Path(settings.MEDIA_ROOT) / str(self.user) / 'uploaded'
        choices = [
            (str(file_path), file_path.name)
            for file_path in user_directory.iterdir()
        ]
        self.fields['image'].choices = choices

    @property
    def uploaded_images(self):
        user_directory = Path(settings.MEDIA_ROOT) / str(self.user) / 'uploaded'
        return [
            f'/media/{self.user}/uploaded/{file_path.name}'
            for file_path in user_directory.iterdir()
        ]


def validate_image_extension(value):
    if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError('Only PNG and JPG images are allowed.')

class ImageUploadForm(forms.Form):
    image = forms.ImageField(validators=[validate_image_extension])