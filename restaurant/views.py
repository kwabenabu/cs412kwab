# file views.py
# author Kwabena Ampomah
# description Views for the restaurant app

import random
from django.shortcuts import render
import time
from django.http import HttpRequest, HttpResponse
from datetime import timedelta
import random as py_random
from django.utils import timezone
daily_specials = [
    {
        "name": "Spaghetti and Meatballs",
        "cost": "$12.99",
        "detail": "Classic Italian pasta dish with homemade meatballs and marinara sauce."
    },
    {
        "name": "Chicken Alfredo",
        "cost": "$14.99",
        "detail": "Creamy Alfredo sauce over tender grilled chicken and fettuccine pasta."
    },
    {
        "name": "Caesar Salad",
        "cost": "$10.99",
        "detail": "Crisp romaine lettuce, Parmesan cheese, croutons, and Caesar dressing."
    },
    {
        "name": "Grilled Salmon",
        "cost": "$18.99",
        "detail": "Fresh salmon fillet grilled to perfection, served with seasonal vegetables."
    },
    {
        "name": "Tacos",
        "cost": "$9.99",
        "detail": "Soft tortillas filled with seasoned beef, lettuce, cheese, and salsa."
    },
    {
        "name": "Vegetable Stir Fry",
        "cost": "$11.99",
        "detail": "A medley of fresh vegetables stir-fried in a savory sauce, served with rice."
    },
    {
        "name": "Beef Stroganoff",
        "cost": "$15.99",
        "detail": "Tender beef strips cooked in a creamy mushroom sauce, served over egg noodles."
    },
]
image=[
    "https://i.snap.as/6ceFxmK3.png"
]
MENU_ITEMS = {
    "pizza": {"name": "Pizza", "price": 12.00},
    "burger": {"name": "Burger", "price": 9.00},
    "salad": {"name": "Salad", "price": 7.00},
    "drink": {"name": "Drink", "price": 2.00},
}

TOPPINGS = {
    "pepperoni": {"name": "Pepperoni", "price": 0.00},
    "mushrooms": {"name": "Mushrooms", "price": 0.00},
    "onions": {"name": "Onions", "price": 0.00},
}
# Create your views here.
def show_main(request):
    template_name = 'restaurant/main.html'
    context = {
        "image": random.choice(image),
    }

    return render(request, template_name, context)

def order_page(request):
    from django.utils import timezone as djtz
    if request.method == "POST":
        # getting all the items into a list because tis simpler
        # citations https://docs.djangoproject.com/en/5.2/ref/request-response/#django.http.HttpRequest.POST
        # get list seems to be the simplest especialy i dont have to make get for each item 

        items = request.POST.getlist("items")
        toppings = request.POST.getlist("pizza_toppings")
        #from the videos it is simple 
        name = request.POST.get("customer_name", "")
        phone = request.POST.get("customer_phone", "")
        email = request.POST.get("customer_email", "")
        instructions = request.POST.get("instructions", "")
        #interger to calculate each total
        total = 0
        #appending the ordered items to a list
        ordered = []
        # this keeps the random item synced to the confirmation page
        special_name = request.POST.get("special_name", "")
        special_cost = request.POST.get("special_cost", "")
        # No need for detail on confirmation, but you can add it if you want
        for i in items:
            # if the item exist int he item list get the price of the item
            if i == "pizza":
                total += 12
                ordered.append("Pizza ($12.00)")
            if i == "burger":
                total += 9
                ordered.append("Burger ($9.00)")
            if i == "salad":
                total += 7
                ordered.append("Salad ($7.00)")
            if i == "drink":
                total += 2
                ordered.append("Drink ($2.00)")
            if i == "special":
                try:
                    #docuemntation for type casting and repalce is from cs111
                    price = float(special_cost.replace("$", ""))
                    #https://docs.python.org/3/library/stdtypes.html#str.replace
                except:
                    # if price is 0 no need
                
                    price = 0
                # add the price to thte total to display it
                total += price
                #add the name and cost to the order 
                ordered.append(f"{special_name} ({special_cost})")
        #https://docs.djangoproject.com/en/5.2/topics/i18n/timezones/#django.utils.timezone.localtime
        #citations for calculation of time 
        local_now = timezone.localtime(timezone.now())
        ready_time = (local_now + timedelta(minutes=random.randint(30, 60))).strftime("%I:%M %p")
        context = {
            "customer_name": name,
            "customer_phone": phone,
            "customer_email": email,
            "selected_items": ordered,
            "pizza_toppings": toppings,
            "instructions": instructions,
            "ready_time": ready_time,
            "total": "$" + str(total),
        }
        return render(request, 'restaurant/confirmation.html', context)
    else:
        template_name = 'restaurant/order.html'
        daily_special = random.choice(daily_specials)
        context = {
            "daily_special": daily_special,
            "daily_specialcost": daily_special["cost"],
            "daily_specialdetail": daily_special["detail"],
        }
        return render(request, template_name, context)
    
def confirmation(request):

    template_name = 'restaurant/confirmation.html'
    print(request.POST)
   
    if request.method == "POST":
        selected_items = request.POST.getlist("items")
        pizza_toppings = request.POST.getlist("pizza_toppings")
        instructions = request.POST.get("instructions", "")
        customer_name = request.POST.get("customer_name", "")
        customer_phone = request.POST.get("customer_phone", "")
        customer_email = request.POST.get("customer_email", "")
    else:
        selected_items = []
        pizza_toppings = []
        instructions = ""
        customer_name = "No name provided"
        customer_phone = "No phone number provided"
        customer_email = "No email provided"
    # Calculate a random ready time between 30 and 60 minutes from now using my ready minutes variable
    ready_minutes = random.randint(30, 60)
    ready_time = (timezone.now() + timedelta(minutes=ready_minutes)).strftime("%I:%M %p")
    context = {
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "customer_email": customer_email,
        "selected_items": selected_items,
        "pizza_toppings": pizza_toppings,
        "instructions": instructions,
        "ready_time": ready_time,
    }
    return render(request, template_name, context=context)
