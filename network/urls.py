
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("following", views.following_posts, name="following"),
    path("profile/<int:user_id>", views.profile, name="profile"),

    # APIs
    path("api/follow/<int:user_id>", views.toggle_follow_unfollow, name="follow"),
    path("api/unfollow/<int:user_id>", views.toggle_follow_unfollow, name="unfollow"),
    path("api/like/<int:post_id>", views.like, name="like"),
    path("api/isuserpost/<int:post_id>", views.is_user_post, name="is_user_post"),
    path("api/post/<int:post_id>", views.post, name="post"),
]
