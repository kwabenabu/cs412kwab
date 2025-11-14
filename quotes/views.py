# File: views.py
# Author: Kwabena Ampomah kwabamp@bu.edu, 3/24/2006
# Description: Our first Python program, in which we demonstrate 
# writing output to the console window.


from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
import random
#global varaible list of quotes and images
QUOTES = [
        "The philosophers have only interpreted the world, in various ways. The point, however, is to change it. — Karl Marx",
        "The history of all hitherto existing society is the history of class struggles. — Karl Marx",
        "From each according to his ability, to each according to his needs. — Karl Marx",
    ]
IMAGES = [
        "https://i.snap.as/6ceFxmK3.png",
        "https://www.marxists.org/archive/marx/photo/marx/images/82km1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Karl-Marx_%28cropped%29.jpg/250px-Karl-Marx_%28cropped%29.jpg"
    ]

# Create your views here.
def main_page(request):
    '''fund to respond to the "home" request. '''
    #template name = 'quotes/main.html'
    #random choice is from python library random https://docs.python.org/3/library/random.html
    #grabbing random choice from the list of quotes and images
    context = {
        "quote": random.choice(QUOTES),
        "image": random.choice(IMAGES),
    }
    return render(request, 'quotes/quote.html', context)
def quotes_page(request):
    '''Respond to the Url 'quotes', deleegate work to a templage'''
    template_name ='quotes/quote.html'
    #grabbing random choice from the list of quotes and images
    context ={
       "quote": random.choice(QUOTES),
       "image": random.choice(IMAGES),
    }
    return render(request, template_name, context)
def show_all_page(request):
    '''Respond to the Url 'show_all'''
    template_name = 'quotes/show_all.html'
    #all quotes and images
    context = {
        "quotes": QUOTES,
        "images": IMAGES
    }
    return render(request, template_name, context)
def about_page(request):
    '''Respond to the Url 'about'''
    template_name ='quotes/about.html'
    context ={
    }
    return render(request, template_name, context)
