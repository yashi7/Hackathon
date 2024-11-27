from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import joblib
import pandas as pd
from django.shortcuts import render
from .models import Restaurant, Event,new_user,DonationRequest
import joblib


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant

@login_required
def upload(request):
    if request.method == 'POST':
        # Get all POST data
            form_data = request.POST.dict()  # Converts QueryDict to a standard dictionary

            # Print each key-value pair (for debugging purposes)
            print("Form Data:")
            for key, value in form_data.items():
                print(f"{key}: {value}")
            
            # Extract data with default values for missing fields
            category = request.POST.get("category", "Not Provided")
            location = request.POST.get("location", "Not Provided")
            locality = request.POST.get("locality", "Not Provided")
            city = request.POST.get("city", "Not Provided")
            cuisine = request.POST.get("cuisine", "Not Provided")
            
            # Restaurant-specific fields
            rating = request.POST.get("rating", None)  # Could be None or not provided
            votes = request.POST.get("votes", None)
            cost = request.POST.get("cost", None)

            # Event-specific fields (can be handled in another model or part of your form)
            type_of_food = request.POST.get("type_of_food", "Not Provided")
            number_of_guests = request.POST.get("number_of_guests", "Not Provided")
            event_type = request.POST.get("event_type", "Not Provided")
            quantity_of_food = request.POST.get("quantity_of_food", "Not Provided")
            storage_conditions = request.POST.get("storage_conditions", "Not Provided")
            purchase_history = request.POST.get("purchase_history", "Not Provided")
            seasonality = request.POST.get("seasonality", "Not Provided")
            preparation_method = request.POST.get("preparation_method", "Not Provided")
            geographical_location = request.POST.get("geographical_location", "Not Provided")
            pricing = request.POST.get("pricing", "Not Provided")

        # Save the restaurant details to the Restaurant model (or another model if needed)
            if rating and votes and cost:  # Ensure that the restaurant-specific data is valid
                restaurant = Restaurant(
                    location=location,
                    locality=locality,
                    city=city,
                    cuisine=cuisine,
                    rating=float(rating),  # Make sure rating is a float
                    votes=int(votes),  # Make sure votes is an integer
                    cost=float(cost)  # Make sure cost is a float
                )
                restaurant.save()

            else:
                event = Event(
                    type_of_food=type_of_food,
                    number_of_guests=number_of_guests,
                    event_type=event_type,
                    quantity_of_food=quantity_of_food,
                    storage_conditions=storage_conditions,
                    purchase_history=purchase_history,
                    seasonality=seasonality,
                    preparation_method=preparation_method,
                    geographical_location=geographical_location,
                    pricing=pricing,
                )
                event.save()

            # Redirect to a confirmation page or back to the upload form
            return redirect('upload')  # Or another view for confirmation
        
    else:
            # Handle case where the restaurant data is not complete (invalid data)
            return render(request, 'upload.html', {'error': 'Please fill out all required fields.'})

    return render(request, 'upload.html')




def insights(request):
    # Example data for insights
    insights_data = {
        "total_donations": 120,
        "total_ngo": 30,
        "total_restaurants": 50,
        "most_active_ngo": "Helping Hands",
        "most_generous_restaurant": "Foodie's Delight",
    }
    return render(request, 'insights.html', insights_data)


def map_view(request):
    # Sample data (replace with database queries)
    restaurants = [
        {"name": "Restaurant A", "latitude": 12.9716, "longitude": 77.5946},
        {"name": "Event B", "latitude": 12.9756, "longitude": 77.5999},
    ]

    ngos = [
        {"name": "NGO 1", "latitude": 12.9656, "longitude": 77.5946, "food_status": "red"},
        {"name": "NGO 2", "latitude": 12.9616, "longitude": 77.5999, "food_status": "yellow"},
        {"name": "NGO 3", "latitude": 12.9516, "longitude": 77.5899, "food_status": "green"},
    ]

    context = {
        "restaurants": restaurants,
        "ngos": ngos,
    }
    return render(request, "get_organizations.html",context)

def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST': 
        logout(request)
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('UserName')
        email = request.POST.get('email') 
        type = request.POST.get('type') 
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        new_user_instance = new_user(username=username, email=email, Type=type)
        new_user_instance.save()
        return redirect('login')

    return render(request, 'signup.html')


def profile(request):
    return render(request, 'profile.html')


def aboutus(request):
    return render(request, 'aboutus.html')

# @login_required
# def upload(request):

#     if request.method == 'POST':
#         image = request.FILES.get('item-image')
#         print(image)
#         # category = request.POST.get('item-category')
#         #gender,category,color,occassion

#         print(request.POST)
#         print("the image is",image)
#         # print("the category is",category)
#         print("the type is:",type(image))


#         if image:
#             user_instance = new_user.objects.filter(username=request.user.username)[0]
#             fs = FileSystemStorage()
#             filename = fs.save(image.name, image)  # Save image to media folder
#             image_url = fs.url(filename)

#             my_wardrobe=Wardrobe(u_id=user_instance,img_path=image,image_name=image.name)
#             my_wardrobe.save()

#             category,color,occassion=predict(image)

#             my_category = Category(w_id=my_wardrobe, u_id=user_instance, Category=category, Color=color, Occassion=occassion)
#             my_category.save()

#             print(category,color,occassion)
#             return redirect('upload')
#         else:
#             return render(request, 'upload.html', {'error': 'All fields are required'})
#     return render(request,'upload.html')

# def insights(request):
#     # Aggregate data: Count how many times each occasion appears in `rec`
#     data_of_cat = (Rec.objects.values('c_id__Occassion')  # Use the related name
#                   .annotate(total=Count('c_id'))
#                   .order_by('c_id__Occassion'))
#     print("data is :",data_of_cat)
#     # Prepare data for Chart.js
#     occasions = [entry['c_id__Occassion'] for entry in data_of_cat]
#     counts_of_ocassions = [entry['total'] for entry in data_of_cat]

    # data_of_cat_wardrobe = (Wardrobe.objects.values('c_id__Occassion')  # Use the related name
    #               .annotate(total=Count('c_id'))
    #               .order_by('c_id__Occassion'))
    # print("data is :",data_of_cat)
    # # Prepare data for Chart.js
    # occasions = [entry['c_id__Occassion'] for entry in data_of_cat]
    # counts_of_ocassions = [entry['total'] for entry in data_of_cat]

    # data_of_color = (Rec.objects.values('c_id__Color')  # Use the related name
    #               .annotate(total=Count('c_id'))
    #               .order_by('c_id__Color'))
    # print("data_of_color is :",data_of_color)
    # # Prepare data for Chart.js
    # colors = [entry['c_id__Color'] for entry in data_of_color]
    # counts_of_colors = [entry['total'] for entry in data_of_color]

    # fav_Color_data = (Favourites.objects.values('c_id__Color')  # Use the related name
    #               .annotate(total=Count('c_id'))
    #               .order_by('c_id__Color'))
    # fav_colors = [entry['c_id__Color'] for entry in fav_Color_data]
    # fav_counts_of_colors = [entry['total'] for entry in fav_Color_data]


    # fav_Cat_data = (Favourites.objects.values('c_id__Occassion')  # Use the related name
    #               .annotate(total=Count('c_id'))
    #               .order_by('c_id__Occassion'))
    # fav_cat = [entry['c_id__Occassion'] for entry in fav_Cat_data]
    # fav_counts_of_cat = [entry['total'] for entry in fav_Cat_data]

    # context = {
    #     'occasions': occasions,
    #     'counts_of_ocassions': counts_of_ocassions,
    #     'colors':colors,
    #     'counts_of_colors':counts_of_colors,
    #     'fav_counts_of_colors':fav_counts_of_colors,
    #     'fav_colors':fav_colors,
    #     'fav_cat':fav_cat,
    #     'fav_counts_of_cat':fav_counts_of_cat,

    # }
    # # print("occasions is :",occasions)
    # # print("counts_of_ocassions is :",counts_of_ocassions)
    # return render(request, 'insights.html', context) 




# @outdated
# def insights(request):
#     current_user = new_user.objects.get(email=request.user.email)

#     # Data for 'Most Worn Items'
#     most_worn_items = Wardrobe.objects.filter(u_id=current_user).values_list('image_name', flat=True)
#     times_worn_data = [5, 12, 7, 3]  # Placeholder data (replace with actual times worn)

#     # Data for 'Color Distribution'
#     color_stats = Category.objects.filter(u_id=current_user).values('Color').annotate(count=Count('Color')).order_by('-count')
#     color_labels = [color['Color'] for color in color_stats]
#     color_data = [color['count'] for color in color_stats]

#     # Data for 'Seasonal Preferences'
#     summer_percent = 30  # Replace with actual data
#     winter_percent = 20
#     spring_percent = 25
#     fall_percent = 25

#     # Data for 'Favorite Categories'
#     category_stats = Category.objects.filter(u_id=current_user).values('Category').annotate(count=Count('Category')).order_by('-count')
#     category_labels = [category['Category'] for category in category_stats]
#     category_data = [category['count'] for category in category_stats]

#     return render(request, 'insights.html', {
#         'most_worn_items': list(most_worn_items),
#         'times_worn_data': times_worn_data,
#         'color_labels': color_labels,
#         'color_data': color_data,
#         'summer_percent': summer_percent,
#         'winter_percent': winter_percent,
#         'spring_percent': spring_percent,
#         'fall_percent': fall_percent,
#         'category_labels': category_labels,
#         'category_data': category_data
#     })


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_donation_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ngo_name = data.get('ngoName')
            food_needed = data.get('foodNeeded')
            donor_name = data.get('donorName')
            donor_contact = data.get('donorContact')

            # Save the donation request (you should create a DonationRequest model)
            donation_request = DonationRequest(
                ngo_name=ngo_name,
                food_needed=food_needed,
                donor_name=donor_name,
                donor_contact=donor_contact
            )
            donation_request.save()

            return JsonResponse({"message": "Donation request sent successfully!"})

        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=400)

    return JsonResponse({"message": "Invalid request"}, status=400)

# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Donation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_invoice(request, donation_id):
    print(donation_id,"............................")
    try:
        donation = get_object_or_404(Donation, id=donation_id)
    except:
        return render(request, 'generate_invoice.html')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{donation_id}.pdf"'

    # Generate PDF
    p = canvas.Canvas(response, pagesize=letter)
    
    p.setFont("Helvetica", 12)
    
    # Add content to the PDF
    p.drawString(100, 750, f"Tax Deduction Invoice for Donation #{donation.id}")
    p.drawString(100, 730, f"Donor: {donation.donor}")
    p.drawString(100, 710, f"Recipient: {donation.recipient}")
    p.drawString(100, 690, f"Quantity Donated: {donation.quantity}")
    p.drawString(100, 670, f"Date of Donation: {donation.date}")
    
    # Add any other details as needed
    p.drawString(100, 650, f"Amount for Tax Deduction: {donation.amount_donated}")
    
    # Close the PDF document
    p.showPage()
    p.save()
    # return response
    return render(request, 'generate_invoice.html')
# views.py
from django.shortcuts import render
from .models import Donation

def view_donations(request):
    donations = Donation.objects.filter(donor_name=request.user.username)  # Assuming you associate donations with the user
    return render(request, 'view_donations.html', {'donations': donations})
def profile(request):
    return render(request, 'profile.html')