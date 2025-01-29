from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="post")
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} posted {self.content} at {self.created_at}"



class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", null=True)
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower", null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followee'], name='unique_follower_followee')
        ]

    def __str__(self):
        try:
            return f"{self.follower.username} follows {self.followee.username}"
        except AttributeError:
            return "Follower or followee is not valid!"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_liked")

    def __str__(self):
        return f"{self.user} liked Post ID: {self.post.id}"