from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Post, Stories
from .forms import PostForm, PhotosForm, ShortsForm, StoriesForm, CommentStories
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Follow, Photo, Shorts
from django.http import JsonResponse
from django.contrib.auth.models import User  # Use this if you're using the default User model
from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def delete_image(request):
    if request.method == "POST":
        data = json.loads(request.body)
        image_type = data.get("image_type")

        if image_type == "profile_pic":
            if request.user.profile_pic:
                request.user.profile_pic.delete()  # Delete the file from storage
                request.user.profile_pic = None
                request.user.save()
        elif image_type == "cover_pic":
            if request.user.cover_pic:
                request.user.cover_pic.delete()  # Delete the file from storage
                request.user.cover_pic = None
                request.user.save()
        else:
            return JsonResponse({"error": "Invalid image type"}, status=400)

        return JsonResponse({"message": "Image deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def helper(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()
    return render(request, 'users/helper.html', {
        'friend_requests_count':friend_requests_count
    })

@login_required
def delete_account(request):
    # Get the blocked users
    blocked_users = request.user.blocked_users.all()
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('profile')  # Redirect to the homepage or a goodbye page

    # Pass the blocked users to the template
    return render(request, 'users/settings.html', {'blocked_users': blocked_users, 'friend_requests_count':friend_requests_count})

def terms(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    return render(request, 'users/terms.html', {
        'friend_requests_count':friend_requests_count
    })
from django.utils.timezone import now, timedelta


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('get_started')  # Make sure 'get_started' URL is defined in urls.py
        else:
            # If form is invalid, render the form again with error messages
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def update_online_status(request):
    if request.method == 'POST':
        user = request.user
        user.last_seen = now()
        user.is_online = True
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def check_user_online_status():
    """Utility function to mark users offline if inactive."""
    timeout = timedelta(minutes=1)  # Define the timeout for online status
    inactive_users = CustomUser.objects.filter(is_online=True, last_seen__lt=now() - timeout)
    inactive_users.update(is_online=False)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    he_posts = Shorts.objects.filter(user__in=following_users)


    user = request.user
    query = request.GET.get('q', '')  # Get search query from GET request
    posts = Photo.objects.filter(user=request.user).order_by('-created_at')  # Get all posts initially
    
    # If there's a query, filter posts based on the query
    if query:
        posts = posts.filter(
            Q(caption__icontains=query) | Q(category__icontains=query)
        )  # Adjust fields to your model
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    # Process the posts and annotate them with additional data
    for post in posts:
        post.has_liked = post.likes_photo.filter(user=request.user).exists()
        post.comments_list = post.comments.all()  # Correctly fetch comments

    # Handle comment submission
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user to the post
            post.save()  # Save the post
            messages.success(request, 'Post created successfully!')
            return redirect('post_results')  # Redirect to the posts list page
    else:
        form = PostForm()
    if request.method == "POST":
        comment_form = CommentPhoto(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Photo, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('photos_list')  # Replace with your URL name
    else:
        comment_form = CommentPhoto()
    user = request.user  # Current logged-in user
    profile_user = user  # You can change this to another user profile if needed (e.g., view other user's profile)
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    is_friend = request.user.friends.filter(id=user.id).exists() if request.user.is_authenticated else False
    friends = user.friends.all()
    if request.method == 'POST':
        if 'follow' in request.POST:
            # Create a follow relationship
            Follow.objects.create(follower=request.user, following=profile_user)
        elif 'unfollow' in request.POST:
            # Remove the follow relationship
            Follow.objects.filter(follower=request.user, following=profile_user).delete()

        # Redirect to the same profile page to update the follow/unfollow status
        return redirect('profile')  # Make sure to adjust this URL name if necessary
    friend_count = user.friends.count()
    return render(request, 'users/profile.html', {
        'user': profile_user,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'friend_requests':friend_requests,
        'friend_requests_count':friend_requests_count,
        'is_friend': is_friend,
        'friends': friends,
        'friend_count':friend_count,
        'posts':posts,
        'he_posts':he_posts,
        'form':form,
    })



@login_required
def users_list(request):
    query = request.GET.get('q', '')  # Get search query from GET request
    user = request.user  # Get the currently logged-in user
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    profile_user = user
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    # Filter users based on the search query and exclude the logged-in user
    users = CustomUser.objects.filter(username__icontains=query).exclude(id=user.id)

    return render(request, 'users/users_list.html', {
        'users': users,  # Pass the filtered list of users into the context
        'query': query,
        'friend_requests':friend_requests ,
        'friend_requests_count':friend_requests_count,
        'followers_count':followers_count,
        'following_count':following_count
    })
def get_started(request):
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    return render(request, 'users/get_started.html', {'friend_requests_count':friend_requests_count})


def person_detail(request, name):
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    # Define the information for each person
    people = {
        "Zikirzoda Faridun": {
            "role": "Founder, Master and Commander, Programmer",
            "description": "Founder, Commander and main programmer. Zikirzoda Faridun make network.",
            "skills":"Programmer",
        },
        "Zikirzoda Abubakr": {
            "role": "Business Stuff, Corporate Stuff and CFO",
            "description": "Responsible for financial strategies.",
            "skills":"Lawyer and prosecutor",
        },
        "Zikirzoda Bobojon": {
            "role": "Graphic designer, main mathematics, ideas designer",
            "description": "Leads creative and mathematical designs.",
            "skills":"Main mathematic",
        },
        "Zikirzoda Abdukhalil": {
            "role": "Ideas and graphic designer, General financial problem solver",
            "description": "Innovator and financial problem solver.",
            "skills":"Businessman",
        },
    }

    # Get the person's info or show a default message
    person_info = people.get(name, {
        "role": "Unknown",
        "description": "This person is not listed in the system.",
        "skills": "This person is not listed in the system.",
    })

    return render(request, 'users/people.html', {
        'name': name,
        'role': person_info['role'],
        'description': person_info['description'],
        'skills': person_info['skills'],
        'friend_requests_count':friend_requests_count,
    })

from .forms import CommentPhoto
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Photo, Follow, FriendRequest
from .forms import CommentPhoto

@login_required
def photos_list(request):
    user = request.user
    profile = request.user
    query = request.GET.get('q', '')  # Get search query from GET request
    posts = Photo.objects.all().order_by('-created_at')  # Get all posts initially
    # If there's a query, filter posts based on the query
    if query:
        posts = posts.filter(
            Q(caption__icontains=query) | Q(category__icontains=query)
        )  # Adjust fields to your model
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    # Process the posts and annotate them with additional data
    for post in posts:
        post.has_liked = post.likes_photo.filter(user=request.user).exists()
        post.comments_list = post.comments.all()  # Correctly fetch comments

    # Handle comment submission
    if request.method == "POST":
        comment_form = CommentPhoto(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Photo, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('photos_list')  # Replace with your URL name
    else:
        comment_form = CommentPhoto()

    # Calculate total comments for all posts
    total_comments = sum(post.comments.count() for post in posts)

    return render(request, 'users/photos_list.html', {
        'posts': posts,  # Pass filtered posts to the template
        'query': query,
        'is_following': is_following,
        'friend_requests': friend_requests,
        'friend_requests_count': friend_requests_count,
        'total_comments': total_comments,  # Use this variable in the template
        'comment_form': comment_form,  # Pass the comment form to the template
        'profile':profile
    })
from django.urls import reverse

@login_required
def search_page(request):
    """ Renders the search bar page. """
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET.get('q', '')
        posts = Shorts.objects.all().order_by('-created_at')  # All posts initially
        
    # Filter posts based on the search query
        for post in posts:
            post.has_liked = post.likes_short.filter(user=request.user).exists()

        # Redirect to results page with the query in the URL
        return redirect(reverse('shorts_results') + f'?q={query}')
    return render(request, 'users/search_page.html', {
        'friend_requests_count':friend_requests_count
    })


@login_required
def recomand(request):
    query = request.GET.get('q', '')  # Search query from GET request
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Shorts.objects.filter(user__in=following_users)  # All posts initially

    # Filter posts based on the search query
    for post in posts:
        post.has_liked = post.likes_short.filter(user=request.user).exists()
        post.comments_list = post.comments.all()  # Correctly fetch comments
    # If there's a query, filter posts based on the query
    if query:
        posts = posts.filter(Q(caption__icontains=query) | Q(category__icontains=query))
    if request.method == "POST":
        comment_form = CommentShort(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Shorts, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('shorts_results')  # Replace with your URL name

    else:
        comment_form = CommentShort()
    # Additional context (e.g., notifications)
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    return render(request, 'users/recomandation.html', {
        'posts': posts,
        'query': query,
        'friend_requests_count': friend_requests_count
    })

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def shorts_results(request):
    query = request.GET.get('q', '')  # Search query from GET request
    posts = Shorts.objects.all().order_by('-created_at')  # Fetch posts initially

    # If there's a query, filter posts based on the query
    if query:
        posts = posts.filter(
            Q(caption__icontains=query) | 
            Q(category__icontains=query)
        )

    # Attach additional data for each post
    for post in posts:
        post.has_liked = post.likes_short.filter(user=request.user).exists()
        post.comments_list = post.comments.all()

    if request.method == "POST":
        comment_form = CommentShort(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Shorts, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('shorts_results')  # Adjust redirect as needed

    else:
        comment_form = CommentShort()

    # Additional context (e.g., notifications)
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    return render(request, 'users/shorts_results.html', {
        'posts': posts,
        'query': query,
        'friend_requests_count': friend_requests_count,
        'comment_form': comment_form,  # Include the form in the context
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Shorts
from .forms import ShortsForm
@login_required
def edit_shorts(request, shorts_id):
    # Get the shorts post belonging to the logged-in user
    shorts = get_object_or_404(Shorts, id=shorts_id, user=request.user)

    if request.method == "POST":
        if "delete" in request.POST:  # Check if the delete button was clicked
            shorts.delete()
            return redirect('shorts_results')  # Replace with the appropriate redirect URL
        else:
            form = ShortsForm(request.POST, request.FILES, instance=shorts)
            if form.is_valid():
                form.save()
                return redirect('shorts_results')  # Replace with the appropriate redirect URL
    else:
        form = ShortsForm(instance=shorts)

    return render(request, 'users/edit_shorts.html', {
        'form': form,
        'shorts': shorts,
    })


@login_required
def photos_results(request):
    query = request.GET.get('q', '')  # Search query from GET request
    posts = Photo.objects.all().order_by('-created_at')  # All posts initially

    # Filter posts based on the search query
    for post in posts:
        post.has_liked = post.likes_photo.filter(user=request.user).exists()
        post.comments_list = post.comments.all()  # Correctly fetch comments
    # If there's a query, filter posts based on the query
    if query:
        posts = posts.filter(Q(caption__icontains=query) | Q(category__icontains=query))
    if request.method == "POST":
        comment_form = CommentPhoto(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Photo, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('photos_results')  # Replace with your URL name

    else:
        comment_form = CommentPhoto()
    # Additional context (e.g., notifications)
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    return render(request, 'users/photo_results.html', {
        'posts': posts,
        'query': query,
        'friend_requests_count': friend_requests_count
    })


@login_required
def post_results(request):
    query = request.GET.get('q', '')  # Search query from GET request
    posts = Post.objects.all().order_by('-created_at')  # All posts initially

    # Filter posts based on the search query
    for post in posts:
        post.has_liked = post.likes.filter(user=request.user).exists()
        post.comments_list = post.comments.all()  # Correctly fetch comments
    # If there's a query, filter posts based on the query
    if query:
        posts = posts.filter(Q(caption__icontains=query) | Q(category__icontains=query))
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Photo, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('post_results')  # Replace with your URL name

    else:
        comment_form = CommentForm()
    # Additional context (e.g., notifications)
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    return render(request, 'users/post_results.html', {
        'posts': posts,
        'query': query,
        'friend_requests_count': friend_requests_count
    })

from .forms import CommentShort
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shorts, FriendRequest
from .forms import CommentShort


from .forms import CommentFlyer
from .models import Flyer
@login_required
def flyer_list(request):
    query = request.GET.get('q', '')  # Get search query from GET request
    posts = Flyer.objects.all().order_by('-created_at')  # Get all posts initially
    for post in posts:
        post.comments_list = post.comments.all()  # Correctly fetch comments
    # If there's a query, filter posts based on the query
    if query:
        post.has_liked = post.likes.filter(user=request.user).exists()
        posts = posts.filter(Q(title__icontains=query) | Q(description__icontains=query))  # Adjust fields to your model
    
    is_following = False
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    if request.method == "POST":
        comment_form = CommentFlyer(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Flyer, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('flyer_list')  # Replace with your URL name

    else:
        comment_form = CommentFlyer()

    return render(request, 'users/flyer_list.html', {
        'posts': posts,  # Pass filtered posts to the template
        'query': query,
        'is_following': is_following,
        'friend_requests': friend_requests,
        'friend_requests_count': friend_requests_count
    })


@login_required
def stories_list(request):
    query = request.GET.get('q', '')  # Get search query from GET request
    posts = Stories.objects.all().order_by('-created_at')  # Get all posts initially
    for post in posts:
        post.has_liked = post.likes_stories.filter(user=request.user).exists()
        post.comments_list = post.comments.all()  # Correctly fetch comments
    # If there's a query, filter posts based on the query
    if query:
        post.has_liked = post.likes.filter(user=request.user).exists()
        posts = posts.filter(Q(title__icontains=query) | Q(description__icontains=query))  # Adjust fields to your model
    
    is_following = False
    user = request.user
    profile_user = user
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    if request.method == "POST":
        comment_form = CommentStories(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Stories, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('stories_list')  # Replace with your URL name

    else:
        comment_form = CommentStories()

    return render(request, 'users/stories_list.html', {
        'posts': posts,  # Pass filtered posts to the template
        'query': query,
        'is_following': is_following,
        'friend_requests': friend_requests,
        'friend_requests_count': friend_requests_count
    })
@login_required
def create_short(request):

    if request.method == 'POST':
        form = ShortsForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user to the post
            post.save()  # Save the post
            messages.success(request, 'Shorts created successfully!')
            return redirect('shorts_results')  # Redirect to the posts list page
    else:
        form = ShortsForm()

    return render(request, 'users/create_short.html', {'form': form})

from .forms import FlyerForm
@login_required
def create_flyer(request):

    if request.method == 'POST':
        form = FlyerForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user to the post
            post.save()  # Save the post
            messages.success(request, 'Flyer created successfully!')
            return redirect('flyer_list')  # Redirect to the posts list page
    else:
        form = FlyerForm()

    return render(request, 'users/create_flyer.html', {'form': form})



@login_required
def create_stories(request):

    if request.method == 'POST':
        form = StoriesForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user to the post
            post.save()  # Save the post
            messages.success(request, 'Stories created successfully!')
            return redirect('stories_list')  # Redirect to the posts list page
    else:
        form = StoriesForm()

    return render(request, 'users/create_stories.html', {'form': form})


@login_required
def create_photo(request):
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    if request.method == 'POST':
        form = PhotosForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user to the post
            post.save()  # Save the post
            messages.success(request, 'Photos created successfully!')
            return redirect('photos_results')  # Redirect to the posts list page
    else:
        form = PhotosForm()

    return render(request, 'users/create_photo.html', {'form': form, 'friend_requests_count':friend_requests_count})

@login_required
def create_post(request, user):
    profile_user = user
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user to the post
            post.save()  # Save the post
            messages.success(request, 'Post created successfully!')
            return redirect('post_results')  # Redirect to the posts list page
    else:
        form = PostForm()

    return render(request, 'users/create_post.html', {'form': form, 'followers_count':followers_count, 'following_count':following_count})

@login_required
def user_profile(request, username):
    # Get the user profile
    user = get_object_or_404(CustomUser, username=username)

    # Get follower/following counts
    
    followers_count = user.followers.count()
    following_count = user.following.count()

    # Get followers and following lists
    followers = user.followers.all()
    following = user.following.all()

    # Get user's music files (limit to the latest 5)
    music_list = user.music_files.all()[:5]  # For example, showing only the latest 5 music files

    # Fetch all posts made by the user, ordered by most recent first
    posts = Photo.objects.filter(user=user).order_by('-created_at')

    # Get all friend requests for the logged-in user
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()
    blocked_users = request.user.blocked_users.all()

    # Check if the logged-in user is following this user
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    # Check if they are already friends
    is_friend = request.user.friends.filter(id=user.id).exists() if request.user.is_authenticated else False

    # Check if there are any sent or received friend requests
    sent_request = FriendRequest.objects.filter(from_user=request.user, to_user=user, status='sent').first()
    received_request = FriendRequest.objects.filter(from_user=user, to_user=request.user, status='sent').first()

    # Get the number of friends
    friend_count = user.friends.count()
    friends = user.friends.all()

    # Render the user profile page with all the necessary data
    return render(request, 'users/user_profile.html', {
        'user': user,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'followers': followers,
        'following': following,
        'is_friend': is_friend,
        'sent_request': sent_request,
        'received_request': received_request,
        'friends': friends,
        'friend_count': friend_count,
        'friend_requests': friend_requests,
        'friend_requests_count': friend_requests_count,
        'music_list': music_list,
        'posts': posts,  # Include posts here
        'blocked_users':blocked_users
    })

@login_required
def show_following(request, username):
    # Get the user profile
    user = get_object_or_404(CustomUser, username=username)

    # Get the following list
    following = user.following.all()


    # Render the page with the following data
    return render(request, 'users/show_following.html', {
        'user': user,
        'following': following,
    })

@login_required
def show_followers(request, username):
    # Get the user profile
    user = get_object_or_404(CustomUser, username=username)

    # Get the following list
    followers = user.followers.all()

    # Render the page with the following data
    return render(request, 'users/show_followers.html', {
        'user': user,
        'followers': followers,
    })

@login_required
def show_friends(request, username):
    # Get the user profile
    user = get_object_or_404(CustomUser, username=username)

    # Get the friends list
    friends = user.friends.all()

    # Render the page with the friends data
    return render(request, 'users/show_friends.html', {
        'user': user,
        'friends': friends,
    })


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if created:
            messages.success(request, f"You are now following {user_to_follow.username}.")
        else:
            messages.info(request, f"You are already following {user_to_follow.username}.")
    
    return redirect('user_profile', username=user_to_follow.username)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    follow_relationship = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
    
    if follow_relationship.exists():
        follow_relationship.delete()
        messages.success(request, f"You have unfollowed {user_to_unfollow.username}.")
    else:
        messages.warning(request, f"You are not following {user_to_unfollow.username}.")
    
    return redirect('user_profile', username=user_to_unfollow.username)
from .models import FriendRequest



@login_required
def inbox(request):
    # Get all pending friend requests for the logged-in user
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    accepted_requests = FriendRequest.objects.filter(to_user=request.user, status='accepted')

    # Get the declined friend requests
    declined_requests = FriendRequest.objects.filter(to_user=request.user, status='declined')
    return render(request, 'users/inbox.html', {
        'friend_requests': friend_requests,
        'accepted_requests': accepted_requests,
        'declined_requests': declined_requests,
        'friend_requests_count': friend_requests_count
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import FriendRequest
@login_required
# Send a friend request
def send_friend_request(request, user_id):
    if request.method == "POST":
        to_user = get_object_or_404(CustomUser, id=user_id)
        from_user = request.user

        # Check if a friend request already exists
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return redirect('user_profile', username=to_user.username)

        if from_user == to_user:
            return redirect('user_profile', username=to_user.username)

        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return redirect('user_profile', username=to_user.username)
    return redirect('user_profile', username=to_user.username)
@login_required
# Accept a friend request
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.to_user == request.user:
        # Accept the friend request by adding to each user's friend list
        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)

        # Update the status of the request to 'accepted'
        friend_request.status = 'accepted'
        friend_request.delete()


        return redirect('user_profile', username=friend_request.from_user.username)

    else:
        # Handle error if the request is not for the current user
        return redirect('error_page')


@login_required
# Decline a friend request
def decline_friend_request(request, request_id):
    if request.method == "POST":
        friend_request = get_object_or_404(FriendRequest, id=request_id)

        if friend_request.to_user != request.user:
            return redirect('user_profile', username=request.user.username)

        # Just delete the friend request
        friend_request.delete()
        return redirect('user_profile', username=friend_request.to_user.username)

    return redirect('user_profile', username=request.user.username)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import CommentForm

@login_required
def post_list(request):
    posts = Post.objects.order_by('-created_at')


    # Determine posts liked by the user
    profile_user = request.user
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    # Add a flag and fetch comments for each post
    for post in posts:
        post.has_liked = post.likes.filter(user=request.user).exists()
        post.comments_list = post.comments.all()  # Correctly fetch comments

    # Handle comment submission
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Post, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('post_list')  # Replace with your URL name

    else:
        comment_form = CommentForm()

    return render(request, 'users/post_list.html', {'posts': posts, 'comment_form': comment_form, 'friend_requests_count': friend_requests_count, 'followers_count': followers_count, 'following_count':following_count})

from django.shortcuts import render, get_object_or_404
from .models import Post, Photo, Shorts, Flyer, Stories, CommentPhoto
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def my_post_list(request):
    user = request.user
    query = request.GET.get('q', '')  # Get search query from GET request
    
    # Get posts and photos made by the current user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    photos = Photo.objects.filter(user=user).order_by('-created_at')
    shorts = Shorts.objects.filter(user=user).order_by('-created_at')
    flyers = Flyer.objects.filter(user=user).order_by('-created_at')
    stories = Stories.objects.filter(user=user).order_by('-created_at')
    
    # Apply search filter if a query exists
    if query:
        posts = posts.filter(Q(caption__icontains=query) | Q(category__icontains=query))
        photos = photos.filter(Q(caption__icontains=query) | Q(category__icontains=query))
        shorts = shorts.filter(Q(caption__icontains=query) | Q(category__icontains=query))
        flyers = flyers.filter(Q(caption__icontains=query) | Q(category__icontains=query))
        stories = stories.filter(Q(caption__icontains=query) | Q(category__icontains=query))
    
    # Check if the user is following themselves (i.e., is the logged-in user)
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    # Handle comment submissions
    if request.method == "POST":
        comment_form = CommentPhoto(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            post = get_object_or_404(Photo, id=request.POST.get("post_id"))
            comment.post = post
            comment.save()
            return redirect('photos_list')  # Redirect to photos list or your chosen page
    else:
        comment_form = CommentPhoto()

    # Total number of comments on the user's posts
    total_comments = sum(post.comments.count() for post in posts) + sum(photo.comments.count() for photo in photos)

    # Return the posts, photos, etc. in the context
    return render(request, 'users/photos.html', {
        'posts': posts,
        'photos': photos,
        'shorts': shorts,
        'flyers': flyers,
        'stories': stories,
        'query': query,
        'is_following': is_following,
        'total_comments': total_comments,
        'comment_form': comment_form,
    })


@login_required
def create_post(request):
    profile_user = request.user
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_results')
    else:
        form = PostForm()
    return render(request, 'users/create_post.html', {
        'form': form,
        'friend_requests_count':friend_requests_count,
        'followers_count':followers_count,
        'following_count':following_count
        })


from .models import Post

@login_required
def like_photo(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Photo, id=post_id)

        # Check if the user has already liked the post
        if post.likes_photo.filter(user=request.user).exists():
            # Unlike the post (remove like)
            post.likes_photo.filter(user=request.user).delete()
        else:
            # Like the post (add like)
            post.likes_photo.create(user=request.user)

        # Return the updated like count
        return JsonResponse({'success': True, 'like_count': post.likes_photo.count()})
    return JsonResponse({'success': False})

@login_required
def like_short(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Shorts, id=post_id)

        # Check if the user has already liked the post
        if post.likes_short.filter(user=request.user).exists():
            # Unlike the post (remove like)
            post.likes_short.filter(user=request.user).delete()
        else:
            # Like the post (add like)
            post.likes_short.create(user=request.user)

        # Return the updated like count
        return JsonResponse({'success': True, 'like_count': post.likes_short.count()})
    return JsonResponse({'success': False})


@login_required
def like_flyer(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Flyer, id=post_id)

        # Check if the user has already liked the post
        if post.likes_flyer.filter(user=request.user).exists():
            # Unlike the post (remove like)
            post.likes_flyer.filter(user=request.user).delete()
        else:
            # Like the post (add like)
            post.likes_flyer.create(user=request.user)

        # Return the updated like count
        return JsonResponse({'success': True, 'like_count': post.likes_flyer.count()})
    return JsonResponse({'success': False})




@login_required
def like_stories(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Stories, id=post_id)

        # Check if the user has already liked the post
        if post.likes_stories.filter(user=request.user).exists():
            # Unlike the post (remove like)
            post.likes_stories.filter(user=request.user).delete()
        else:
            # Like the post (add like)
            post.likes_stories.create(user=request.user)

        # Return the updated like count
        return JsonResponse({'success': True, 'like_count': post.likes_stories.count()})
    return JsonResponse({'success': False})

@login_required
def like_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        # Check if the user has already liked the post
        if post.likes.filter(user=request.user).exists():
            # Unlike the post (remove like)
            post.likes.filter(user=request.user).delete()
        else:
            # Like the post (add like)
            post.likes.create(user=request.user)

        # Return the updated like count
        return JsonResponse({'success': True, 'like_count': post.likes.count()})
    return JsonResponse({'success': False})
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.auth import get_user_model

User = get_user_model()  # This will give you the custom user model, not 'auth.User'
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from .models import VideoCall
from django.shortcuts import render

def video_call(request):
    return render(request, "users/video_call.html")

@csrf_exempt
def create_call(request):
    if request.method == "POST":
        data = json.loads(request.body)
        caller = request.user
        callee_id = data["callee_id"]

        call = VideoCall.objects.create(caller=caller, callee_id=callee_id)
        return JsonResponse({"call_id": call.id}, status=201)

@csrf_exempt
def send_offer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        call = VideoCall.objects.get(id=data["call_id"])
        call.offer = data["offer"]
        call.save()
        return JsonResponse({"status": "offer saved"}, status=200)

@csrf_exempt
def send_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        call = VideoCall.objects.get(id=data["call_id"])
        call.answer = data["answer"]
        call.save()
        return JsonResponse({"status": "answer saved"}, status=200)

def get_call_data(request, call_id):
    call = VideoCall.objects.get(id=call_id)
    data = {
        "offer": call.offer,
        "answer": call.answer,
        "ice_candidates": call.ice_candidates,
    }
    return JsonResponse(data)
# Then in your views:
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, CustomUser

@login_required
def fetch_new_messages(request, username):
    recipient = get_object_or_404(CustomUser, username=username)
    logged_in_user = request.user

    messages = Message.objects.filter(
        (Q(sender=logged_in_user) & Q(receiver=recipient)) |
        (Q(sender=recipient) & Q(receiver=logged_in_user))
    ).order_by('timestamp')

    messages_data = []
    for message in messages:
        messages_data.append({
            'content': message.content,
            'timestamp': message.timestamp.strftime('%H:%M'),
            'image': message.image.url if message.image else None,
            'video': message.video.url if message.video else None,
            'sender': message.sender.username,
            'is_read': 'fas fa-check-circle' if message.is_read else 'fas fa-times-circle',
        })
    Message.objects.filter(sender=recipient, receiver=logged_in_user, is_read=False).update(is_read=True)

    return JsonResponse({'messages': messages_data})


from django.utils.crypto import get_random_string

@login_required
def chat_with_user(request, username):
    recipient = get_object_or_404(CustomUser, username=username)
    logged_in_user = request.user
    friend_requests_count = FriendRequest.objects.filter(to_user=logged_in_user).count()

    # Fetch all messages between the logged-in user and the recipient
    messages = Message.objects.filter(
        (Q(sender=logged_in_user) & Q(receiver=recipient)) |
        (Q(sender=recipient) & Q(receiver=logged_in_user))
    ).order_by('timestamp')

    # Mark all unread messages from the recipient as read
    Message.objects.filter(sender=recipient, receiver=logged_in_user, is_read=False).update(is_read=True)
    blocked_users = request.user.blocked_users.all()

    # Generate a unique video call room name
    video_call_room = f"chat_{logged_in_user.id}_{recipient.id}_{get_random_string(8)}"

    return render(request, 'users/chat.html', {
        'user': recipient,
        'messages': messages,
        'friend_requests_count': friend_requests_count,
        'video_call_room': video_call_room,  # Pass room name to the template
        'blocked_users':blocked_users,
    })

@login_required
def send_message(request, username):
    if request.method == 'POST':
        recipient = get_object_or_404(CustomUser, username=username)
        sender = request.user

        # Check if the recipient has blocked the sender
        if sender in recipient.blocked_users.all():
            return JsonResponse({'error': "This user has blocked you. You cannot send messages."}, status=403)

        # Check if the sender has blocked the recipient
        if recipient in sender.blocked_users.all():
            return JsonResponse({'error': "You have blocked this user. Unblock them to send messages."}, status=403)

        message_content = request.POST.get('message', '')
        image = request.FILES.get('image', None)
        video = request.FILES.get('video', None)

        if not message_content and not image and not video:
            return JsonResponse({'error': "Message cannot be empty!"}, status=400)

        message = Message.objects.create(
            sender=sender,
            receiver=recipient,
            content=message_content,
            image=image,
            video=video
        )

        message_data = {
            'content': message.content,
            'timestamp': message.timestamp.strftime('%H:%M'),
            'image': message.image.url if message.image else None,
            'video': message.video.url if message.video else None,
            'sender': message.sender.username,
            'is_read': 'fas fa-check-circle' if message.is_read else 'fas fa-times-circle',
        }

        return JsonResponse({'message': message_data})

    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def block_user(request, username):
    user_to_block = get_object_or_404(CustomUser, username=username)
    if user_to_block == request.user:
        return redirect('chat_with_user', username=username)

    request.user.blocked_users.add(user_to_block)
    return redirect('chat_with_user', username=username)

@login_required
def unblock_user(request, username):
    user_to_unblock = get_object_or_404(CustomUser, username=username)
    request.user.blocked_users.remove(user_to_unblock)
    return redirect('chat_with_user', username=username)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Call, CustomUser


def start_call(request, username):
    # Get the user to call
    receiver = get_object_or_404(CustomUser, username=username)

    # Prevent users from calling themselves
    if request.user == receiver:
        return JsonResponse({'error': "You cannot call yourself!"}, status=400)

    # Check if there's an active call between the users
    existing_call = Call.objects.filter(
        caller=request.user, receiver=receiver, is_active=True
    ).first()

    # If an active call exists, redirect to the existing room
    if existing_call:
        return redirect('join_call', room_name=existing_call.room_name)

    # Otherwise, create a new call
    call = Call.objects.create(caller=request.user, receiver=receiver)
    return redirect('join_call', room_name=call.room_name)
def join_call(request, room_name):
    return render(request, 'users/video_call.html', {
        'room_name': room_name,
        'request_user': request.user.username
    })
from django.utils import timezone  # Add this import
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def edit_message(request, message_id):
    try:
        # Fetch the message that the logged-in user sent
        message = Message.objects.get(id=message_id, sender=request.user)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found or permission denied'}, status=404)

    if request.method == 'POST':
        new_content = request.POST.get('message', '').strip()
        if not new_content:
            return JsonResponse({'error': 'Message content cannot be empty'}, status=400)

        # Update the message content and timestamp
        message.content = new_content
        message.timestamp = timezone.now()
        message.save()

        # Return updated message data
        return JsonResponse({
            'message': {
                'content': message.content,
                'timestamp': message.timestamp.strftime('%H:%M'),
            }
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id, sender=request.user)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found or permission denied'}, status=404)

    if request.method == 'POST':
        message.delete()
        return JsonResponse({'success': 'Message deleted successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.shortcuts import render, redirect
from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Replace 'profile' with your profile view's name
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})

from django.core.paginator import Paginator

from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, Count
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Message, FriendRequest, CustomUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Message, FriendRequest, CustomUser
@login_required
def chat_users_list(request):
    logged_in_user = request.user
    
    # Get a list of users the logged-in user has chatted with (based on messages)
    chat_users = Message.objects.filter(
        Q(sender=logged_in_user) | Q(receiver=logged_in_user)
    ).values('sender', 'receiver').distinct()

    # Create a list of unique users
    users = []
    for chat_user in chat_users:
        users.append(chat_user['sender'] if chat_user['sender'] != logged_in_user.id else chat_user['receiver'])

    # Exclude users with pending friend requests
    friend_requests_sent = FriendRequest.objects.filter(from_user=logged_in_user, status='sent')
    friend_requests_received = FriendRequest.objects.filter(to_user=logged_in_user, status='sent')

    # Get users who are friends (exclude pending requests)
    friend_users = CustomUser.objects.filter(id__in=users).exclude(
        id__in=[request.to_user.id for request in friend_requests_received]
    )

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        friend_users = friend_users.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query) | Q(name__icontains=search_query) | Q(surname__icontains=search_query))

    # Fetch the most recent message for each user
    recent_messages = {}
    for user in friend_users:
        last_message = Message.objects.filter(
            Q(sender=user) | Q(receiver=user),
            Q(sender=logged_in_user) | Q(receiver=logged_in_user)
        ).order_by('-timestamp').first()  # Get the most recent message
        recent_messages[user.id] = last_message
    blocked_users = request.user.blocked_users.all()

    # Pagination
    paginator = Paginator(friend_users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch unread messages for each user
    unread_messages = Message.objects.filter(
        receiver=logged_in_user, is_read=False
    ).order_by('timestamp')  # Fetch unread messages, ordered by timestamp

    # Add unread messages to the user data
    friend_users_with_unread_messages = []
    for user in friend_users:
        user_unread_messages = unread_messages.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')

        friend_users_with_unread_messages.append({
            'user': user,
            'unread_messages': user_unread_messages,
            'last_message': recent_messages.get(user.id)  # Add last message
        })

    # Get the friend requests count
    friend_requests_count = FriendRequest.objects.filter(to_user=request.user).count()
    
    return render(request, 'users/chat_users_list.html', {
        'page_obj': page_obj,
        'friend_requests_count': friend_requests_count,
        'friend_users_with_unread_messages': friend_users_with_unread_messages,  # Pass unread messages to the template
        'search_query': search_query,  # Pass the search query to the template
        'blocked_users':blocked_users,
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Group, GroupMessage
from .forms import GroupForm, GroupMessageForm

import logging
logger = logging.getLogger(__name__)

@login_required
def create_group(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    if request.method == 'POST':
        logger.info(f"Uploaded files: {request.FILES}")
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user
            group.save()
            form.save_m2m()
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'users/create_group.html', {'form': form, 'friend_requests_count':friend_requests_count})
@login_required
def fetch_group_messages(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    logged_in_user = request.user

    # Ensure the user is a member of the group
    if logged_in_user not in group.members.all():
        return JsonResponse({'error': 'You are not a member of this group.'}, status=403)

    messages = group.messages.all().order_by('timestamp')

    messages_data = []
    for message in messages:
        # Determine the sender's profile picture or fallback
        sender_profile_pic = message.sender.profile_pic.url if message.sender.profile_pic else (
                    "https://i.pinimg.com/600x315/34/6e/1d/346e1df0044fd77dfb6f65cc086b2d5e.jpg" 
            if message.sender.gender == "M" 
            else "https://i.pinimg.com/1200x/c7/0c/36/c70c3652b86753708079b17e9033c488.jpg"
        )

        # Gather profile pictures for all readers with fallbacks
        readers_profile_pics = []
        for reader in message.readers.all():
            if reader.profile_pic:
                readers_profile_pics.append(reader.profile_pic.url)
            else:
                # Fallback if the reader does not have a profile picture
                fallback_pic = (
                    "https://i.pinimg.com/600x315/34/6e/1d/346e1df0044fd77dfb6f65cc086b2d5e.jpg" 
                    if reader.gender == "M" 
                    else ""
                )
                readers_profile_pics.append(fallback_pic)

        messages_data.append({
            'content': message.content,
            'timestamp': message.timestamp.strftime('%H:%M'),
            'image': message.image.url if message.image else None,
            'video': message.video.url if message.video else None,
            'sender': message.sender.username,
            'sender_profile_pic': sender_profile_pic,
            'is_read': logged_in_user in message.readers.all(),  # Check if the logged-in user has read this
            'readers_profile_pics': readers_profile_pics,  # Add list of readers' profile pictures
        })

    # Mark unread group messages as read for the logged-in user
    unread_messages = group.messages.exclude(readers=logged_in_user)
    unread_messages.update(is_read=True)  # Update the unread messages
    for message in unread_messages:
        message.readers.add(logged_in_user)  # Add the logged-in user to the readers

    return JsonResponse({'messages': messages_data})
@login_required
def group_detail(request, group_id):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()

    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        return redirect('profile')  # Redirect if the user is not a member of the group

    # Fetch all messages in the group
    messages = group.messages.all().order_by('timestamp')

    # Process each message
    for message in messages:
        # Mark the messages as read by the current user
        if request.user not in message.readers.all():
            message.readers.add(request.user)
            message.is_read = True  # Optionally update the 'is_read' field
            message.save()

        # Add sender's gender and profile picture to the message object for template usage
        message.sender_gender = message.sender.gender
        message.sender_profile_pic = message.sender.profile_pic.url if message.sender.profile_pic else None

        # Add readers' profile picture URLs
        message.readers_profile_pics = [
            reader.profile_pic.url if reader.profile_pic else (
                "https://t3.ftcdn.net/jpg/04/43/94/64/360_F_443946404_7GUoIGZeyx7R7ymCicI3k0xPnrMoKDek.webp"
                if reader.gender == "M" else
                "https://media.istockphoto.com/id/1327592664/ru/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F/%D0%B7%D0%BD%D0%B0%D1%87%D0%BE%D0%BA-%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8F-%D1%84%D0%BE%D1%82%D0%BE-%D0%B0%D0%B2%D0%B0%D1%82%D0%B0%D1%80%D0%B0-%D0%BF%D0%BE-%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E-%D1%81%D0%B5%D1%80%D0%BE%D0%B5-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8F-%D0%B4%D0%B5%D0%BB%D0%BE%D0%B2%D0%B0%D1%8F-%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD%D0%B0.jpg?s=170667a&w=0&k=20&c=zSkOCGQKzshhVaqfS6hHsmUYbOQopoz0Z3dcPllf8uE="
            ) for reader in message.readers.all()
        ]

    message_form = GroupMessageForm()

    return render(request, 'users/group_detail.html', {
        'group': group,
        'messages': messages,
        'message_form': message_form,
        'friend_requests_count': friend_requests_count
    })

from .forms import GroupUpdateForm

@login_required
def group_settings(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()
    # Ensure only group admin can access this page
    if request.user != group.admin:
        messages.error(request, "You do not have permission to access group settings.")
        return redirect('profile')

    if request.method == "POST":
        # Update group name
        if 'update_group' in request.POST:
            group_form = GroupUpdateForm(request.POST, instance=group)
            if group_form.is_valid():
                group_form.save()
                messages.success(request, "Group name updated successfully.")
            else:
                messages.error(request, "Failed to update group name.")

        # Add a member
        elif 'add_member' in request.POST:
            username = request.POST.get('new_member')
            try:
                user = User.objects.get(username=username)
                if user not in group.members.all():
                    group.members.add(user)
                    messages.success(request, f"{username} has been added to the group.")
                else:
                    messages.error(request, f"{username} is already a member.")
            except User.DoesNotExist:
                messages.error(request, "User not found.")

        # Remove a member
        elif 'remove_member' in request.POST:
            member_id = request.POST.get('member_id')
            member = get_object_or_404(User, id=member_id)
            if member in group.members.all():
                group.members.remove(member)
                messages.success(request, f"{member.username} has been removed from the group.")
            else:
                messages.error(request, "User is not a member of the group.")

        # Delete the group
        elif 'delete_group' in request.POST:
            group.delete()
            messages.success(request, "Group deleted successfully.")
            return redirect('profile')

    group_form = GroupUpdateForm(instance=group)
    return render(request, 'users/group_settings.html', {
        'group': group,
        'group_form': group_form,
        'friend_requests_count':friend_requests_count
    })


@login_required
def groups(request):
    groups = Group.objects.all()
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_count = friend_requests.count()
    return render(request, 'users/groups.html', {
        'groups':groups,
        'friend_requests_count':friend_requests_count
    })

@login_required
def send_group_message(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    sender = request.user

    # Check if the user is a member of the group
    if sender not in group.members.all():
        return JsonResponse({'error': 'You are not a member of this group.'}, status=403)

    if request.method == 'POST':
        # Get message content and any files (image/video)
        message_content = request.POST.get('message', '')
        image = request.FILES.get('image', None)
        video = request.FILES.get('video', None)

        # Validate if the message or files are provided
        if not message_content and not image and not video:
            return JsonResponse({'error': "Message cannot be empty!"}, status=400)

        # Create the group message
        message = GroupMessage.objects.create(
            sender=sender,
            group=group,
            content=message_content,
            image=image,
            video=video
        )

        # Prepare message data for response
        message_data = {
            'content': message.content,
            'timestamp': message.timestamp.strftime('%H:%M'),
            'image': message.image.url if message.image else None,
            'video': message.video.url if message.video else None,
            'sender': message.sender.username,
        }

        return JsonResponse({'message': message_data})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_member_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user != group.admin:
        return redirect('group_detail', group_id=group.id)  # Only admin can add members

    if request.method == 'POST':
        new_member_id = request.POST.get('new_member_id')
        new_member = get_object_or_404(CustomUser, id=new_member_id)
        group.members.add(new_member)
        return redirect('group_detail', group_id=group.id)

    # Get all users who are not already in the group
    users = CustomUser.objects.exclude(id__in=group.members.values_list('id', flat=True))
    return render(request, 'users/add_member.html', {'group': group, 'users': users})


def custom_404_view(request, exception):
    return render(request, '404.html', {}, status=404)