from django.urls import path
from django.urls import include

from news import views

urlpatterns = [
    path('', views.index, name='index_url'),
    path('<int:id_post>/', views.post_detail, name='post_detail_url'),
    path('<int:id_post>/add_comment', views.add_comment, name='add_comment_url'),
    path('<int:id_post>/post_update/', views.PostUpdate.as_view(), name='post_update_url'),
    path('<int:id_post>/post_delete/', views.PostDelete.as_view(), name='post_delete_url'),
    path('<int:id_tag>/tag_update/', views.TagUpdate.as_view(), name='tag_update_url'),
    path('<int:id_tag>/tag_delete/', views.TagDelete.as_view(), name='tag_delete_url'),
    path('post_create/', views.PostCreate.as_view(), name='post_create_url'),
    path('tag_create/', views.TagCreate.as_view(), name='tag_create_url'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('account/', views.UserUpdateView.as_view(), name='profile_detail_url'),
    path('account/update', views.UserUpdateView.as_view(), name='profile_update_url'),
    path('account/posts', views.UserPostsListView.as_view(), name='user_posts_url')
    # path('', include('news.urls')),
]

