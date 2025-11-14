from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import * 
from .serializers import JokeSerializer, PictureSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
import time

class RandomJokeView(TemplateView):
    template_name = 'dadjokes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['joke'] = Joke.objects.order_by('?').first()
        context['picture'] = Picture.objects.order_by('?').first()

        return context

class JokeListView(ListView):
    template_name = 'dadjokes/show_all_jokes.html'
    model = Joke
    context_object_name = 'jokes'

class JokeDetailView(DetailView):
    template_name = 'dadjokes/show_joke.html'
    model = Joke
    context_object_name = 'joke'



class PictureListView(ListView):
    template_name = 'dadjokes/show_all_pictures.html'
    model = Picture
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    template_name = 'dadjokes/show_picture.html'
    model = Picture
    context_object_name = 'picture'

@api_view(['GET'])
def get_random_joke(request):
    jokes = list(Joke.objects.all())
    pictures = list(Picture.objects.all())
    joke = random.choice(jokes)
    picture = random.choice(pictures)
    joke_serializer = JokeSerializer(joke)
    picture_serializer = PictureSerializer(picture)
    return Response({
        'joke': joke_serializer.data,
        'picture': picture_serializer.data
    })

@api_view(['GET', 'POST'])
def get_all_jokes(request):
    if request.method == 'GET':
        jokes = list(Joke.objects.all())
        serializer = JokeSerializer(jokes, many=True)
        return Response(serializer.data)

    # Handle POST request to create a new joke
    serializer = JokeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_single_joke(request, pk):
    selected_joke = Joke.objects.get(pk=pk)
    serializer = JokeSerializer(selected_joke)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_pictures(request):
    pictures = list(Picture.objects.all())
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_random_picture(request):
    pictures = list(Picture.objects.all())
    picture = random.choice(pictures) if pictures else None
    if picture is None:
        return Response({'detail': 'No pictures available'}, status=404)
    serializer = PictureSerializer(picture)
    return Response(serializer.data)

@api_view(['GET'])
def get_single_picture(request, pk):
    selected_picture = Picture.objects.get(pk=pk)
    serializer = PictureSerializer(selected_picture)
    return Response(serializer.data)
