from django.urls import path
from .views import * #Adds all the view functions that exist
from django.conf.urls.static import static    ## add for static files
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'dadjokes'

urlpatterns = [
    path('', RandomJokeView.as_view(), name="show_random_joke"),
    path('random/', RandomJokeView.as_view(), name="show_random_joke"),
    path('jokes/', JokeListView.as_view(), name="show_all_jokes"),
    path('joke/<int:pk>', JokeDetailView.as_view(), name="show_joke"),
    path('pictures', PictureListView.as_view(), name="show_all_pictures"),
    path('picture/<int:pk>', PictureDetailView.as_view(), name="show_picture"),
    path('api/', get_random_joke, name="random_joke"),
    path('api/random', get_random_joke, name="random_joke"),
    path('api/random_picture', get_random_picture, name="random_picture"),
    path('api/jokes', get_all_jokes, name="jokes"),
    path('api/joke/<int:pk>', get_single_joke, name="single_joke"),
    path('api/pictures', get_all_pictures, name="pictures"),
    path('api/picture/<int:pk>', get_single_picture, name="single_picture"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
