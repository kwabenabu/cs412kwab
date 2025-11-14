"""mini_insta models — Profiles, Posts, and Photos.

Photos can come from an external URL (old way) or a local upload stored in the
project's media folder.
"""

# mini_insta models file
# Author: Kwabena Ampomah
# What's here: Profiles, Posts, and Photos (URL or uploaded file)

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    """User profile information for the mini_insta app."""
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)
    # Associate Profile with Django auth User (initially nullable for migration)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profiles'
    )

    def __str__(self):
        """Return the display name for convenient admin/console display."""
        return f'{self.display_name}'
    
    def get_all_posts(self):
        """Return this profile's posts ordered newest-first by timestamp."""
        return Post.objects.filter(profile=self).order_by('-timestamp')

    # --- Followers / Following accessors ---
    def get_followers(self):
        """Return a list of Profiles who follow this profile."""
        return [f.follower_profile for f in Follow.objects.filter(profile=self)]

    def get_num_followers(self):
        """Return the number of followers for this profile."""
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """Return a list of Profiles that this profile is following."""
        return [f.profile for f in Follow.objects.filter(follower_profile=self)]

    def get_num_following(self):
        """Return the number of profiles this profile is following."""
        return Follow.objects.filter(follower_profile=self).count()

    # --- Feed accessor ---
    def get_post_feed(self):
        """Return Posts from profiles this profile follows, newest first."""
        following_profiles = self.get_following()
        return Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')

    def get_absolute_url(self):
        """Return the URL for this profile's detail page.
        Used by UpdateView to determine where to redirect after a successful
        update operation.
        """
        return reverse('show_profile', kwargs={'pk': self.pk})

class Post(models.Model):
    """A single post belonging to a profile, with a caption and timestamp."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        """Return a readable description containing author and timestamp."""
        return f'Post by {self.profile.display_name} on {self.timestamp.strftime("%Y-%m-%d %H:%M")}'
    
    def get_all_photos(self):
        """Return this post's photos ordered by timestamp (oldest first)."""
        return Photo.objects.filter(post=self).order_by('timestamp')

    def get_all_comments(self):
        """Return all comments on this post ordered by timestamp."""
        return Comment.objects.filter(post=self).order_by('timestamp')

    def get_likes(self):
        """Return all Like objects for this post."""
        return Like.objects.filter(post=self)

class Photo(models.Model):
    """A photo for a post, from either a URL (legacy) or uploaded file."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Keep existing URL for backward-compatibility
    image_url = models.URLField(blank=True)
    # New: uploaded image stored in Django media directory
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable description with storage type and timestamp."""
        storage = 'URL' if self.image_url else 'File'
        return f'Photo ({storage}) for post by {self.post.profile.display_name} on {self.timestamp.strftime("%Y-%m-%d %H:%M")}'

    def get_image_url(self):
        """Return a usable URL for this photo.

        Prefers the legacy `image_url` if present; otherwise returns the
        `image_file.url` for uploaded images. Returns an empty string if no
        URL is available.
        """
        if self.image_url:
            return self.image_url
        if self.image_file:
            try:
                return self.image_file.url
            except ValueError:
                # File might not be available yet
                return ''
        return ''


class Follow(models.Model):
    """A follow relationship: follower_profile follows profile."""
    # Note: assignment requests these related_name values
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile"
    )  # the publisher being followed
    follower_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follower_profile"
    )  # the subscriber who follows
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"


class Comment(models.Model):
    """A comment by a profile on a post."""
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        preview = (self.text[:30] + '…') if len(self.text) > 30 else self.text
        return f"Comment by {self.profile.display_name} on {self.post.profile.display_name}'s post: {preview}"


class Like(models.Model):
    """A like by a profile on a post."""
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.display_name} liked a post by {self.post.profile.display_name}"
