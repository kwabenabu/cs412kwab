from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Main landing page showing all available apps"""
    apps = [
        {'name': 'Admin Panel', 'url': '/admin/', 'description': 'Django admin interface'},
        {'name': 'HW App', 'url': '/hw/', 'description': 'Homework examples'},
        {'name': 'Quotes App', 'url': '/quotes/', 'description': 'Quote of the day website'},
        {'name': 'Restaurant App', 'url': '/restaurant/', 'description': 'Krusty Krab restaurant website'},
        {'name': 'Dad Jokes App', 'url': '/dadjokes/', 'description': 'Premium dad jokes and pictures'},
        {'name': 'Mini Instagram', 'url': '/mini_insta/', 'description': 'Mini Instagram clone'},
        {'name': 'Voter Analytics', 'url': '/voter_analytics/', 'description': 'Voter data analytics'},
    ]
    
    context = {'apps': apps}
    return render(request, 'home.html', context)
