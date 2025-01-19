from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import Post, Comment, Photo, Shorts, Stories
from .models import CommentFlyer
from .models import Flyer
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'surname', 'email', 'gender', 'status', 'profile_pic', 'cover_pic']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'mini_info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short Bio', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
            'cover_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
            
        }
class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class PhotosForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['caption', 'image', 'category']
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        caption = cleaned_data.get('caption')

        if not caption:
            raise forms.ValidationError("Text posts must have a caption.")
        if not image:
            raise forms.ValidationError("Image posts must have an image.")
        return cleaned_data

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'category']
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What is in your mind?'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        caption = cleaned_data.get('caption')

        if not caption:
            raise forms.ValidationError("Text posts must have a caption.")
        return cleaned_data

class ShortsForm(forms.ModelForm):
    class Meta:
        model = Shorts
        fields = ['caption', 'video', 'category']
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        caption = cleaned_data.get('caption')

        if not caption:
            raise forms.ValidationError("Text posts must have a caption.")
        if not video:
            raise forms.ValidationError("Video and Short posts must have a video.")
        if video and video.size > 60 * 1024 * 1024:
            raise forms.ValidationError("Short videos must be less than 1 minute.")
        return cleaned_data
    

class FlyerForm(forms.ModelForm):
    class Meta:
        model = Flyer
        fields = ['caption', 'video', 'category']
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        caption = cleaned_data.get('caption')

        if not caption:
            raise forms.ValidationError("Text posts must have a caption.")
        if not video:
            raise forms.ValidationError("Video and Short posts must have a video.")
        if video and video.size > 60 * 1024 * 1024:
            raise forms.ValidationError("Short videos must be less than 1 minute.")
        return cleaned_data
    



class StoriesForm(forms.ModelForm):
    class Meta:
        model = Stories
        fields = ['caption', 'video', 'category']
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        caption = cleaned_data.get('caption')

        if not caption:
            raise forms.ValidationError("Stories posts need have a caption.")
        if not video:
            raise forms.ValidationError("Video and Stories posts must have a video.")
        if video and video.size > 60 * 1024 * 1024:
            raise forms.ValidationError("Stories videos must be less than 1 minute.")
        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
from .models import CommentPhoto
class CommentPhoto(forms.ModelForm):
    class Meta:
        model = CommentPhoto
        fields = ['content']
from .models import CommentShorts
class CommentShort(forms.ModelForm):
    class Meta:
        model = CommentShorts
        fields = ['content']
class CommentFlyer(forms.ModelForm):
    class Meta:
        model = CommentFlyer
        fields = ['content']
from .models import CommentStories
class CommentStories(forms.ModelForm):
    class Meta:
        model = CommentStories
        fields = ['content']
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'surname', 'email', 'number', 'gender', 'mini_info', 'status', 'music', 'profile_pic', 'cover_pic', 'accounts_type', 'website', 'profile_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'mini_info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short Bio', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
            'cover_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
            'accounts_type': forms.Select(attrs={'class': 'form-control'}),
            'profile_type': forms.Select(attrs={'class': 'form-control'}),
            'music': forms.ClearableFileInput(attrs={
                'class': 'form-control-file', 
                'accept': 'audio/*',  # Accept only audio files
                'placeholder': 'Upload Music',
                'style': 'background-color: #f3f3f3; padding: 10px; border-radius: 5px; border: 1px solid #ccc;'
            }),
            'website': forms.TextInput(attrs={
            'placeholder': 'Enter your website URL',
            'class': 'form-control',  # Add any custom class for styling
            'style': 'width: 100%; padding: 8px; border-radius: 4px;'
        })
        }


from django import forms
from .models import Group, GroupMessage
from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'members', 'group_image']  # Include group_image here
        widgets = {
            'members': forms.CheckboxSelectMultiple(),  # Optional: customize member selection
        }

class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['content', 'image', 'video']
from django import forms
from .models import Group

class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
