from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.timezone import now

class CustomUser(AbstractUser):
    blocked_users = models.ManyToManyField('self', symmetrical=False, related_name='blocked_by', blank=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    username = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    number= models.PositiveIntegerField(null=True, blank=True)
    surname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    mini_info = models.TextField(max_length=200, blank=True)
    friends = models.ManyToManyField('self', blank=True)
    music = models.FileField(upload_to='user_music/', blank=True, null=True)
    TYPE_CHOISE = [
        ('O', 'Open'),
        ('C', 'Close - request'),
        ('F', 'Friend - request')

    ]
    PROF_CHOISE = [
        ('C', 'Company'),
        ('P', 'Default - profile'),
        ('S', 'Online store')

    ]
    accounts_type = models.CharField(max_length=1, choices=TYPE_CHOISE, default='O')
    profile_type = models.CharField(max_length=1, choices=PROF_CHOISE, default='P')
    status_choices = [
        ('greate', 'Greate 😎'),
        ('good', 'Good 😍'),
        ('normal', 'Normal 😐'),
        ('sad', 'Sad 😔'),
        ('bad', 'Bad 😡'),
        ('super_bad', 'Super Bad 🤬'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='normal')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    cover_pic = models.ImageField(upload_to='cover_pics/', blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.name} {self.surname}'

class UserMusic(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="music_files")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='user_music/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Post(models.Model):

    CATEGORIES = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('news', 'News'),
        ('sports', 'Sports'),
        ('others', 'Others'),
    ]

    user = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)
    caption = models.TextField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='others')  # New category field
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Post by {self.user.username} - {self.caption[:30] if self.caption else 'No Caption'}"

    def total_likes(self):
        return self.likes.count()
class Photo(models.Model):

    CATEGORIES = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('news', 'News'),
        ('sports', 'Sports'),
    ]

    user = models.ForeignKey(CustomUser, related_name='photos', on_delete=models.CASCADE)
    caption = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, blank=True, null=True)  # New category field
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Photo by {self.user.username} - {self.caption[:30] if self.caption else 'No Caption'}"

    def total_likes(self):
        return self.likes_photo.count()
class Shorts(models.Model):

    CATEGORIES = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('news', 'News'),
        ('sports', 'Sports'),
    ]

    user = models.ForeignKey(CustomUser, related_name='shorts', on_delete=models.CASCADE)
    caption = models.TextField(max_length=500, blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, blank=True, null=True)  # New category field
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Post by {self.user.username} - {self.caption[:30] if self.caption else 'No Caption'}"

    def total_likes(self):
        return self.like_shorts.count()
    
class Flyer(models.Model):

    CATEGORIES = [
        ('home', 'Home'),
        ('clothes', 'Clothes'),
        ('items', 'Items'),
        ('devices', 'Devices'),
        ('others','Others'),
    ]

    user = models.ForeignKey(CustomUser, related_name='flyer', on_delete=models.CASCADE)
    caption = models.TextField(max_length=500, blank=True, null=True)
    video = models.FileField(upload_to='posts/flyer/videos', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='others')  # New category field
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Post by {self.user.username} - {self.caption[:30] if self.caption else 'No Caption'}"

    def total_likes(self):
        return self.likes_flyer.count()

from datetime import timedelta
from django.utils import timezone

class Stories(models.Model):
    CATEGORIES = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('news', 'News'),
        ('sports', 'Sports'),
    ]

    user = models.ForeignKey(CustomUser, related_name='stories', on_delete=models.CASCADE)
    caption = models.TextField(max_length=500, blank=True, null=True)
    video = models.FileField(upload_to='posts/stories/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post by {self.user.username} - {self.caption[:30] if self.caption else 'No Caption'}"

    def total_likes(self):
        return self.likes_stories.count()

    def is_older_than_24_hours(self):
        return self.created_at < timezone.now() - timedelta(hours=24)

    @classmethod
    def delete_old_stories(cls):
        old_stories = cls.objects.filter(created_at__lt=timezone.now() - timedelta(hours=24))
        old_stories.delete()


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

class LikePhoto(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Photo, related_name='likes_photo', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

class LikeShort(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Shorts, related_name='likes_short', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)


class LikeFlyer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Flyer, related_name='likes_flyer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

class LikeStories(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Stories, related_name='likes_stories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

class CommentPhoto(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Photo, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=now)

class CommentShorts(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Shorts, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=now)

class CommentFlyer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Flyer, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=now)

class CommentStories(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Stories, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=now)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=now)


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"



class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='sent')

    def __str__(self):
        return f"Request from {self.from_user} to {self.to_user} ({self.status})"
class Chat(models.Model):
    users = models.ManyToManyField(CustomUser)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {', '.join([user.username for user in self.users.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)  # Text content (optional)
    image = models.ImageField(upload_to='messages/images/', blank=True, null=True)  # Image upload (optional)
    video = models.FileField(upload_to='messages/videos/', blank=True, null=True)  # Video upload (optional)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

class Group(models.Model):
    name = models.CharField(max_length=255)  # Group name
    group_image = models.ImageField(upload_to='group_images/', blank=True)
    admin = models.ForeignKey(CustomUser, related_name='admin_groups', on_delete=models.CASCADE)  # Group admin
    members = models.ManyToManyField(CustomUser, related_name='group_memberships')  # Members of the group
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)  # Reference to the group
    sender = models.ForeignKey(CustomUser, related_name='group_messages', on_delete=models.CASCADE)  # Message sender
    content = models.TextField(blank=True, null=True)  # Text content (optional)
    image = models.ImageField(upload_to='group_messages/images/', blank=True, null=True)  # Image upload (optional)
    video = models.FileField(upload_to='group_messages/videos/', blank=True, null=True)  # Video upload (optional)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Optional: Track if the message is read
    readers = models.ManyToManyField(CustomUser, related_name='read_messages', blank=True)


    def __str__(self):
        return f"Message in {self.group.name} by {self.sender.username} at {self.timestamp}"


from django.db import models
from django.conf import settings
from django.utils.timezone import now

class VideoCall(models.Model):
    caller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="outgoing_calls", on_delete=models.CASCADE)
    callee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="incoming_calls", on_delete=models.CASCADE)
    offer = models.TextField(blank=True, null=True)  # SDP offer
    answer = models.TextField(blank=True, null=True)  # SDP answer
    ice_candidates = models.TextField(blank=True, null=True)  # JSON-encoded ICE candidates
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return f"Call from {self.caller.username} to {self.callee.username}"
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string

class Call(models.Model):
    caller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='calls_initiated',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='calls_received',
        on_delete=models.CASCADE
    )
    room_name = models.CharField(max_length=100, unique=True, default=get_random_string(12))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Call from {self.caller} to {self.receiver}"
