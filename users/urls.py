from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

handler404 = 'users.views.custom_404_view'

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('terms', views.terms, name='terms'),
    path('users/', views.users_list, name='users_list'),
    path('all_photos/', views.photos_list, name='photos_list'),
    path('create_post/', views.create_post, name='create_post'),
    path('@<str:username>/', views.user_profile, name='user_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('get-started/', views.get_started, name='get_started'),
    path('inbox/', views.inbox, name='inbox'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('all_posts/', views.post_list, name='post_list'),
    path('all_photos/', views.photos_list, name='photos_list'),
    path('photos/', views.my_post_list, name='my_post_list'),
    path('all_flyers', views.flyer_list, name='flyer_list'),
    path('all_stories', views.stories_list, name='stories_list'),
    path('like/', views.like_post, name='like_post'),
    path('like_photo/', views.like_photo, name='like_photo'),
    path('like_shorts/', views.like_short, name='like_short'),
    path('like_flyer/', views.like_flyer, name='like_flyer'),
    path('like_stories/', views.like_stories, name='like_stories'),
    path('create-post/', views.create_post, name='create_post'),
    path('create-short/', views.create_short, name='create_short'),
    path('create-flyer/', views.create_flyer, name='create_flyer'),
    path('create-stories/', views.create_stories, name='create_stories'),
    path('create-photo/', views.create_photo, name='create_photo'),
    path('chat/<str:username>/', views.chat_with_user, name='chat_with_user'),
    path('chat-users/', views.chat_users_list, name='chat_users_list'),
    path('send-message/<str:username>/', views.send_message, name='send_message'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('person/<str:name>/', views.person_detail, name='person_detail'),  # Dynamic URL for person details
    path('shorts/search/', views.search_page, name='search_page'),       # Page 1: Search Bar
    path('shorts/results/', views.shorts_results, name='shorts_results'),
    path('home/', views.recomand, name='recomand'),
    path('photo/results/', views.photos_results, name='photos_results'), # Page 2: Results Page
    path('post/results/', views.post_results, name='post_results'), # Page 2: Results Page
    path('user/<str:username>/following/', views.show_following, name='show_following'),
    path('user/<str:username>/friends/', views.show_friends, name='show_friends'),
    path('user/<str:username>/followers/', views.show_followers, name='show_followers'),
    path('shorts/edit/<int:shorts_id>/', views.edit_shorts, name='edit_shorts'),
    path('chat/<str:username>/fetch/', views.fetch_new_messages, name='fetch_new_messages'),
    path("video-call/", views.video_call, name="video_call"),
    path('message/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('update-online-status/', views.update_online_status, name='update_online_status'),
    path('call/start/<str:username>/', views.start_call, name='start_call'),
    # URL for joining the call
    path('call/join/<str:room_name>/', views.join_call, name='join_call'),
    path('settings/', views.delete_account, name='delete_account'),
    path('block/<str:username>/', views.block_user, name='block_user'),
    path('unblock/<str:username>/', views.unblock_user, name='unblock_user'),
    path('helper/', views.helper, name='helper'),
    path("delete-image/", views.delete_image, name="delete_image"),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/', views.groups, name='groups'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/fetch/', views.fetch_group_messages, name='fetch_group_messages'),    path('groups/<int:group_id>/send_message/', views.send_group_message, name='send_group_message'),
    path('groups/<int:group_id>/add_member/', views.add_member_to_group, name='add_member_to_group'),
    path('groups/<int:group_id>/settings/', views.group_settings, name='group_settings'),

]