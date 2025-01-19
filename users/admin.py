from django.contrib import admin
from .models import CustomUser, Post, Photo, Shorts, Stories, Like, LikePhoto, LikeShort, LikeStories, Comment, CommentPhoto, CommentShorts, CommentStories, Follow, FriendRequest, Chat, Message, UserMusic

from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'gender', 'status', 'get_blocked_users', 'get_password')
    search_fields = ('username', 'email')
    list_filter = ('gender', 'status')
    filter_horizontal = ('blocked_users',)  # Multi-select for managing blocked users

    # Admin action to block a user
    def block_user(self, request, queryset):
        for user in queryset:
            # Add the selected users to the blocked_users list of the logged-in admin
            request.user.blocked_users.add(user)
        self.message_user(request, "Selected users have been blocked.")

    block_user.short_description = "Block selected users"

    # Admin action to unblock a user
    def unblock_user(self, request, queryset):
        for user in queryset:
            # Remove the selected users from the blocked_users list of the logged-in admin
            request.user.blocked_users.remove(user)
        self.message_user(request, "Selected users have been unblocked.")

    unblock_user.short_description = "Unblock selected users"

    # Display blocked users in the admin
    def get_blocked_users(self, obj):
        return ", ".join([user.username for user in obj.blocked_users.all()])
    get_blocked_users.short_description = 'Blocked Users'

    # Display password hash (or a placeholder text)
    def get_password(self, obj):
        return "********"  # You can return a placeholder or hashed password
    get_password.short_description = 'Password'

    actions = ['block_user', 'unblock_user']  # Add actions to the admin panel

# Register the CustomUser model with the admin


# Post Admin
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'category', 'created_at', 'total_likes')
    search_fields = ('user__username', 'caption', 'category')
    list_filter = ('category', 'created_at')

    def total_likes(self, obj):
        return obj.total_likes()
    total_likes.short_description = 'Likes Count'

# Photo Admin
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'category', 'created_at', 'total_likes')
    search_fields = ('user__username', 'caption', 'category')
    list_filter = ('category', 'created_at')

    def total_likes(self, obj):
        return obj.total_likes()
    total_likes.short_description = 'Likes Count'

# Shorts Admin
class ShortsAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'category', 'created_at', 'total_likes')
    search_fields = ('user__username', 'caption', 'category')
    list_filter = ('category', 'created_at')

    def total_likes(self, obj):
        return obj.total_likes()
    total_likes.short_description = 'Likes Count'

# Stories Admin
class StoriesAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'category', 'created_at', 'total_likes', 'is_older_than_24_hours')
    search_fields = ('user__username', 'caption', 'category')
    list_filter = ('category', 'created_at')

    def total_likes(self, obj):
        return obj.total_likes()
    total_likes.short_description = 'Likes Count'

    def is_older_than_24_hours(self, obj):
        return obj.is_older_than_24_hours()
    is_older_than_24_hours.short_description = 'Older Than 24 Hours'

# Like Admin (for all Like models)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__caption')
    list_filter = ('created_at',)

# Follow Admin
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    list_filter = ('created_at',)

# Friend Request Admin
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'timestamp')
    search_fields = ('from_user__username', 'to_user__username')
    list_filter = ('status', 'timestamp')

# Chat Admin
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'get_users')
    search_fields = ('users__username',)
    list_filter = ('created_at',)

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    get_users.short_description = 'Users in Chat'

# Message Admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('is_read', 'timestamp')

# User Music Admin
class UserMusicAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'uploaded_at')
    search_fields = ('user__username', 'title')
    list_filter = ('uploaded_at',)

# Register Models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Shorts, ShortsAdmin)
admin.site.register(Stories, StoriesAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(LikePhoto, LikeAdmin)
admin.site.register(LikeShort, LikeAdmin)
admin.site.register(LikeStories, LikeAdmin)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    search_fields = ('content', 'user__username', 'post__caption')
    list_filter = ('created_at', 'post__category')

# Registering the CommentAdmin for the Comment model
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentPhoto, CommentAdmin)
admin.site.register(CommentShorts, CommentAdmin)
admin.site.register(CommentStories, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserMusic, UserMusicAdmin)
