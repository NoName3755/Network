from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like

import json


def index(request):
    posts = Post.objects.all()

    p = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_posts = p.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]

        if len(content) >= 1:
            post = Post(user=request.user, content=content)
            post.save()
        
        return HttpResponseRedirect(reverse('index'))



def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_posts = Post.objects.filter(user=user)

    following_count = user.following.all().count()
    followers_count = user.follower.all().count()

    p = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    posts = p.get_page(page_number)

    is_following = False
    if request.user != user:
        for follow in request.user.following.all():
            if follow.followee == user:
                is_following = True

    return render(request, "network/index.html", {
        "posts": posts,
        "profile_user": user,
        "in_profile": True,
        "is_following": is_following,
        "following_count": following_count,
        "followers_count":followers_count,
    })


def following_posts(request):
    if request.user.is_authenticated:
        posts = []
        for follow in request.user.following.all():
            for post in follow.followee.post.all():
                posts.append(post)

        posts.sort(reverse=True, key=lambda a: a.created_at)
        
        p = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_posts = p.get_page(page_number)

        return render(request, "network/index.html", {
            "posts": page_posts,
            "in_following": True,
        })
    
    return HttpResponseRedirect(reverse("index"))


# api
@login_required
def toggle_follow_unfollow(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "The user is not signned in."}, status=400)

    if request.user.id == user_id:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    try:
        follow_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"User with {user_id} does not exists."}, status=400)

    followers_count = follow_user.follower.all().count()

    # Check whether the user is following or not
    is_following = False
    for follow in request.user.following.all():
        if follow.followee == follow_user:
            is_following = True
            # Delete follow data if user is following
            follow.delete()
            
            return JsonResponse({
                "followers_count": followers_count - 1,
                "message": "Unfollow is successful!"
            }, status=200)
    
    if not is_following:
        new_follow = Follow()
        new_follow.follower = request.user
        new_follow.followee = follow_user
        new_follow.save()
    
        return JsonResponse({
            "followers_count": followers_count + 1,
            "message": "Follow is successful!"
        }, status=200)


# api
def like(request, post_id):
    """
    GET Method:
        Return no. of likes of given post id
        and whether user's like the post
    POST Method:
        toggle like
        Return no. of likes of given post id
        and whether user's like the post
    Return {
        "likes_count": <no of likes>,
        "is_liked": True or False
    }
    """

    try:
        post = Post.objects.get(pk=post_id)

    except Post.DoesNotExist:
        return JsonResponse({
            "error": f"Post id: {post_id} does not exists!"
        }, status=404)

    likes_count = post.likes.all().count()

    # Check if users has liked the post
    is_post_liked_by_user = False
    try:
        if request.user.is_authenticated:
            like = Like.objects.get(user=request.user, post=post)   
            is_post_liked_by_user = True
    except Like.DoesNotExist:
        is_post_liked_by_user = False

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User is not authenticated."}, status=400)
        
        # delete like if user's already liked and add new like if user hasn't liked
        if is_post_liked_by_user:
            like.delete()
            return JsonResponse({
                "likes_count": likes_count - 1,
                "is_liked": False
            }, status=200)
        else:
            new_like = Like(user=request.user, post=post)
            new_like.save()
            return JsonResponse({
                "likes_count": likes_count + 1,
                "is_liked": True
            }, status=200)


    elif request.method == "GET":
        return JsonResponse({
            "likes_count": likes_count,
            "is_liked": is_post_liked_by_user
        }, status=200)

#api
def is_user_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "isUserPost": False
        })

    try:
        post = Post.objects.get(pk=post_id)
        if post.user == request.user:
            return JsonResponse({
                "isUserPost": True
            })

        return JsonResponse({
            "isUserPost": False
        })
    except Post.DoesNotExist:
        return JsonResponse({
            "error": f"Post id: {post_id} does not exists!"
        }, status=404)

#api
def post(request, post_id):
    print("Called")
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "The post does not exist!"}, status=404)
    
    if post.user != request.user:
        return JsonResponse({"error": "User does not own this post."}, ststus=200)

    if request.method == 'GET':
        return JsonResponse({
            "content": post.content
        })

    elif request.method == 'PUT':
        if post.user != request.user:
            return JsonResponse({"error": "User does not own the post."}, status=400)
        
        data = json.loads(request.body)
        content = data.get("content")

        if content:
            post.content = content
            post.save()

            return HttpResponse(status=204)
        else:
            return JsonResponse({"error": "The content is empty."}, status=400)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
