"""Views for the mini_insta app.

Contains simple list/detail views for profiles and posts, a CreateView to
create posts (including photo uploads), and Update/Delete views for profiles
and posts.
"""

# file views.py
# author Kwabena Ampomah
# description Views for the mini_insta app

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Photo, Like, Follow
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from .mixins import AuthMixin

# Create your views here.
class ProfileListView(ListView):
    """List all profiles."""
    model = Profile
    template_name = 'insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    """Show a single profile and its details."""
    model = Profile
    template_name = 'insta/show_profile.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        """Add flags for ownership and follow state for the logged-in user."""
        context = super().get_context_data(**kwargs)
        me = None
        if self.request.user.is_authenticated:
            me = Profile.objects.filter(user=self.request.user).order_by('-pk').first()
        context['can_update'] = bool(me and self.object.user_id == self.request.user.id)
        context['can_follow'] = bool(me and me.pk != self.object.pk)
        if me and me.pk != self.object.pk:
            context['is_following'] = Follow.objects.filter(follower_profile=me, profile=self.object).exists()
        else:
            context['is_following'] = False
        return context

class PostDetailView(DetailView):
    """Show a single post with all its photos."""
    model = Post
    template_name = 'insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Add the author's profile for navigation context if needed."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        me = None
        if self.request.user.is_authenticated:
            me = Profile.objects.filter(user=self.request.user).order_by('-pk').first()
        context['can_edit_post'] = bool(me and self.object.profile_id == me.id)
        context['can_like'] = bool(me and self.object.profile_id != me.id)
        context['has_liked'] = bool(me and Like.objects.filter(profile=me, post=self.object).exists())
        return context

class CreatePostView(AuthMixin, CreateView):
    """Create a new post and handle optional photo uploads."""
    model = Post
    form_class = CreatePostForm
    template_name = 'insta/create_post_form.html'
# https://django.readthedocs.io/en/5.2.x/ref/forms/index.html
    def form_valid(self, form):
        """Attach profile, save post, then create Photo objects from uploads."""
        # Attach the logged in user's profile to the post 
        profile = self.get_logged_in_profile()
        form.instance.profile = profile
        
        # Save the post first
        response = super().form_valid(form)
        
        # Previously: create Photo from POST['image_url'] (kept for reference)
        # image_url = self.request.POST.get('image_url')
        # if image_url:
        #     Photo.objects.create(post=self.object, image_url=image_url)

        # Now: handle uploaded files stored in Django's media
        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)
        
        return response
    # https://django.readthedocs.io/en/5.2.x/ref/forms/index.html
    def get_success_url(self):
        """Redirect to the newly created post's detail page."""
        return reverse('show_post', kwargs={'pk': self.object.pk})

class UpdateProfileView(AuthMixin, UpdateView):
    """Update an existing profile using UpdateProfileForm."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'insta/update_profile_form.html'
    # Success URL handled by Profile.get_absolute_url()

    def get_object(self, queryset=None):
        obj = self.get_logged_in_profile()
        if not obj or obj.user_id != self.request.user.id:
            return self.handle_no_permission()
        return obj


class DeletePostView(AuthMixin, DeleteView):
    """Delete a post after user confirmation."""
    model = Post
    template_name = 'insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        """Provide the post and its profile to the template context."""
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        me = self.get_logged_in_profile()
        if not me or obj.profile_id != me.id:
            return self.handle_no_permission()
        return obj

    def get_success_url(self):
        """Redirect to the profile page of the post author after deletion."""
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class UpdatePostView(AuthMixin, UpdateView):
    """Update the caption of a post."""
    model = Post
    fields = ['caption']
    template_name = 'insta/update_post_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        me = self.get_logged_in_profile()
        if not me or obj.profile_id != me.id:
            return self.handle_no_permission()
        return obj

    def get_success_url(self):
        """Redirect to the updated post's detail page."""
        return reverse('show_post', kwargs={'pk': self.object.pk})


class ShowFollowersDetailView(DetailView):
    """DetailView for a Profile to display its followers."""
    model = Profile
    template_name = 'insta/show_followers.html'
    context_object_name = 'profile'


class ShowFollowingDetailView(DetailView):
    """DetailView for a Profile to display profiles it is following."""
    model = Profile
    template_name = 'insta/show_following.html'
    context_object_name = 'profile'


class PostFeedListView(AuthMixin, ListView):
    """ListView that shows the post feed for the logged-in user."""
    template_name = 'insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.profile = self.get_logged_in_profile()
        if not self.profile:
            return Post.objects.none()
        return self.profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class SearchView(AuthMixin, ListView):
    """Search Profiles and Posts. Shows a search form or results."""
    template_name = 'insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.get_logged_in_profile()
        self.query = request.GET.get('query', '').strip()
        if not self.query:
            # No query provided: show the search form
            return render(request, 'insta/search.html', {'profile': self.profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Posts that contain the query in the caption
        return Post.objects.filter(caption__icontains=self.query).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        context['query'] = self.query
        # Profiles that match on display_name or bio_text
        context['matching_profiles'] = Profile.objects.filter(
            Q(display_name__icontains=self.query) | Q(bio_text__icontains=self.query)
        )
        # Posts are provided by get_queryset as 'posts'
        return context


class CreateProfileView(CreateView):
    """Create a Django User and a Profile in one go, then log in."""
    model = Profile
    form_class = CreateProfileForm
    template_name = 'insta/create_profile_form.html'
    success_url = reverse_lazy('show_all_profiles')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_form'] = kwargs.get('user_form') or UserCreationForm()
        return ctx

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # Log the user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Attach to profile
            form.instance.user = user
            return super().form_valid(form)
        # If user form invalid, re-render both forms with errors
        return self.form_invalid(form)


class FollowView(AuthMixin, View):
    def post(self, request, pk):
        me = self.get_logged_in_profile()
        other = get_object_or_404(Profile, pk=pk)
        if me and other and me.pk != other.pk:
            Follow.objects.get_or_create(follower_profile=me, profile=other)
        return redirect(other.get_absolute_url())


class UnfollowView(AuthMixin, View):
    def post(self, request, pk):
        me = self.get_logged_in_profile()
        other = get_object_or_404(Profile, pk=pk)
        if me and other:
            Follow.objects.filter(follower_profile=me, profile=other).delete()
        return redirect(other.get_absolute_url())


class LikeView(AuthMixin, View):
    def post(self, request, pk):
        me = self.get_logged_in_profile()
        post = get_object_or_404(Post, pk=pk)
        if me and post and post.profile_id != me.id:
            Like.objects.get_or_create(profile=me, post=post)
        return redirect(reverse('show_post', kwargs={'pk': pk}))


class UnlikeView(AuthMixin, View):
    def post(self, request, pk):
        me = self.get_logged_in_profile()
        post = get_object_or_404(Post, pk=pk)
        if me and post:
            Like.objects.filter(profile=me, post=post).delete()
        return redirect(reverse('show_post', kwargs={'pk': pk}))
