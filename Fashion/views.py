from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import new_user, Category, Wardrobe
from static.Model.Model_interface import predict
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.db import models
from django.shortcuts import render
from .models import Wardrobe, Category, Favourites, new_user,Rec
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Question, UserAnswer
from django.contrib.auth.decorators import login_required

# Create your views here.


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
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        con_pass = request.POST.get('confirm_password')

        if password != con_pass:
            return redirect('signup')

        my_user = User.objects.create_user(username, email, password)
        my_user.save()

        user = new_user(username=username,
                      email=email,
                      Gender=gender,
                      )
        user.save()
        return redirect('login')
    return render(request, 'signup.html')


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
@login_required
def upload(request):
    print(f"Logged in user: {request.user.username}")
    if request.method == 'POST':
        image = request.FILES.get('item-image')
        folder = request.FILES.getlist('folder-upload')
        print(image)
        print(folder)
        try:
                user_instance = new_user.objects.get(
                    username=request.user.username)
        except new_user.DoesNotExist:
                print(
                    f"No new_user instance found for username: {request.user.username}")
                return render(request, 'upload.html', {'error': 'User information not found. Please sign up again.'})

        fs = FileSystemStorage()

        if image:
            # Attempt to fetch the user's new_user instance safely
            
            filename = fs.save(image.name, image)  # Save image to media folder
            print(filename)
            image_url = fs.url(filename)
            print("IN UPLOAD*******@@@@@@", image_url)
            # Create and save the Wardrobe instance
            my_wardrobe = Wardrobe(
                u_id=user_instance, img_path=image_url, image_name=image.name)
            print("my wardrobe is", my_wardrobe)
            my_wardrobe.save()

            # Use the predict function to get the category, color, and occasion
            category, color, occasion = predict(image)

            # Create and save the Category instance
            my_category = Category(w_id=my_wardrobe, u_id=user_instance,
                                   Category=category, Color=color, Occassion=occasion)
            my_category.save()

            print(category, color, occasion)
            return redirect('upload')  # Adjust redirect based on your URLs
        elif folder:
            for file in folder:
                if file.content_type.startswith('image/'):  # Check if the file is an image
                    filename = fs.save(file.name, file)  # Save each image to media folder
                    image_url = fs.url(filename)
                    print("Folder image URL:", image_url)

                    # Create and save the Wardrobe instance for each image
                    my_wardrobe = Wardrobe(u_id=user_instance, img_path=image_url, image_name=file.name)
                    my_wardrobe.save()

                    # Use the predict function for each image file
                    category, color, occasion = predict(file)

                    # Create and save the Category instance for each image
                    my_category = Category(w_id=my_wardrobe, u_id=user_instance, Category=category, Color=color, Occassion=occasion)
                    my_category.save()

                    print("Folder image details:", category, color, occasion)

            return redirect('upload')
        else:
            return render(request, 'upload.html', {'error': 'All fields are required'})

    return render(request, 'upload.html')



def profile(request):
    return render(request, 'profile.html')

COLOR_COMPATIBILITY = {
    'Black': ['White', 'Red', 'Grey', 'Pink', 'Magenta', 'Orange', 'Yellow'],
    'Blue': ['White', 'Grey', 'Pink', 'Yellow'],
    'Brown': ['Beige', 'White', 'Green', 'Yellow', 'Orange'],
    'Green': ['White', 'Black', 'Brown', 'Yellow'],
    'Grey': ['Black', 'White', 'Pink', 'Blue'],
    'Magenta': ['White', 'Black', 'Grey'],
    'Navy Blue': ['White', 'Yellow', 'Grey', 'Pink'],
    'Orange': ['White', 'Black', 'Brown', 'Yellow'],
    'Pink': ['White', 'Grey', 'Black'],
    'Red': ['White', 'Black', 'Grey', 'Magenta'],
    'White': ['Black', 'Blue', 'Red', 'Yellow', 'Pink'],
    'Yellow': ['Black', 'Blue', 'White', 'Orange'],
}

def recommendation(request):

    if request.method == 'POST':
        occassion_rec = request.POST.get('occassion')
        user_instance = new_user.objects.get(username=request.user.username)
        matching_items = Category.objects.filter(
            Occassion=occassion_rec).filter(u_id=user_instance)
            # Step 2: Initialize recommendation list
        recommendations = []

        # Step 3: Process items for recommendations
        for item in matching_items:
            if item.Category in ['Dress', 'Saree', 'Apparel Set']:
                # Standalone items
                recommendations.append(item)
            if item.Category == 'Topwear':
                # Find compatible Bottomwear
                compatible_bottoms = matching_items.filter(
                    Category='Bottomwear',
                    Color=COLOR_COMPATIBILITY.get(item.Color, [])
                )
                print(compatible_bottoms)
                for bottom in compatible_bottoms:
                    recommendations.append((item, bottom))  # Pair top and bottom

                if len(compatible_bottoms)==0:
                    recommendations.append(item)
            if item.Category == 'Bottomwear':
                # Find compatible Topwear
                compatible_tops = matching_items.filter(
                    Category='Topwear',
                    Color=COLOR_COMPATIBILITY.get(item.Color, [])
                )
                for top in compatible_tops:
                    recommendations.append((top, item))  # Pair top and bottom
                if len(compatible_tops)==0:
                    recommendations.append(item)

         # Step 4: Save recommendations to database
        for recommendation in recommendations:
            if isinstance(recommendation, tuple):  # If it's a pair (Topwear + Bottomwear)
                top, bottom = recommendation
                if not Rec.objects.filter(u_id=user_instance, c_id=top).exists():
                    Rec.objects.create(u_id=user_instance, c_id=top, created_at=timezone.now())
                if not Rec.objects.filter(u_id=user_instance, c_id=bottom).exists():
                    Rec.objects.create(u_id=user_instance, c_id=bottom, created_at=timezone.now())
            else:  # Standalone items
                if not Rec.objects.filter(u_id=user_instance, c_id=recommendation).exists():
                    Rec.objects.create(u_id=user_instance, c_id=recommendation, created_at=timezone.now())

        # Render recommendations in the template
        return render(request, 'recommendation.html', {'recommendations': recommendations,'occassion':occassion_rec})

    return render(request, 'recommendation.html')


@login_required
def view_wardrobe(request):
    try:
        # Get the `new_user` instance of the currently logged-in user
        user_instance = new_user.objects.get(username=request.user.username)

        # Fetch all wardrobe items uploaded by this user
        user_items = Wardrobe.objects.filter(u_id=user_instance)
        user_categories = Category.objects.filter(u_id=user_instance)

    except new_user.DoesNotExist:
        user_items = []  # If the user is not found, show no items
        user_categories = []

    return render(request, 'view_wardrobe.html', {'items': user_items, 'categories': user_categories})


def insights(request):
    # Aggregate data: Count how many times each occasion appears in `rec`
    data_of_cat = (Rec.objects.values('c_id__Occassion')  # Use the related name
                  .annotate(total=Count('c_id'))
                  .order_by('c_id__Occassion'))
    print("data is :",data_of_cat)
    # Prepare data for Chart.js
    occasions = [entry['c_id__Occassion'] for entry in data_of_cat]
    counts_of_ocassions = [entry['total'] for entry in data_of_cat]

    # data_of_cat_wardrobe = (Wardrobe.objects.values('c_id__Occassion')  # Use the related name
    #               .annotate(total=Count('c_id'))
    #               .order_by('c_id__Occassion'))
    # print("data is :",data_of_cat)
    # # Prepare data for Chart.js
    # occasions = [entry['c_id__Occassion'] for entry in data_of_cat]
    # counts_of_ocassions = [entry['total'] for entry in data_of_cat]

    data_of_color = (Rec.objects.values('c_id__Color')  # Use the related name
                  .annotate(total=Count('c_id'))
                  .order_by('c_id__Color'))
    print("data_of_color is :",data_of_color)
    # Prepare data for Chart.js
    colors = [entry['c_id__Color'] for entry in data_of_color]
    counts_of_colors = [entry['total'] for entry in data_of_color]

    fav_Color_data = (Favourites.objects.values('c_id__Color')  # Use the related name
                  .annotate(total=Count('c_id'))
                  .order_by('c_id__Color'))
    fav_colors = [entry['c_id__Color'] for entry in fav_Color_data]
    fav_counts_of_colors = [entry['total'] for entry in fav_Color_data]


    fav_Cat_data = (Favourites.objects.values('c_id__Occassion')  # Use the related name
                  .annotate(total=Count('c_id'))
                  .order_by('c_id__Occassion'))
    fav_cat = [entry['c_id__Occassion'] for entry in fav_Cat_data]
    fav_counts_of_cat = [entry['total'] for entry in fav_Cat_data]

    context = {
        'occasions': occasions,
        'counts_of_ocassions': counts_of_ocassions,
        'colors':colors,
        'counts_of_colors':counts_of_colors,
        'fav_counts_of_colors':fav_counts_of_colors,
        'fav_colors':fav_colors,
        'fav_cat':fav_cat,
        'fav_counts_of_cat':fav_counts_of_cat,

    }
    # print("occasions is :",occasions)
    # print("counts_of_ocassions is :",counts_of_ocassions)
    return render(request, 'insights.html', context) 


def favourite(request):
    if request.user.is_authenticated:
        user_instance = get_object_or_404(new_user, username=request.user.username)
        favorites = Favourites.objects.filter(u_id=user_instance)

        # Prepare a list to hold favorite images and related details
        favorite_items = []
        
        for fav in favorites:
            print("this is fav id",fav.c_id_id)
            # Accessing the Category linked with the favorite
            category = get_object_or_404(Category, c_id=fav.c_id_id)
            # Get the corresponding Wardrobe item
            wardrobe_item = get_object_or_404(Wardrobe, w_id=category.w_id_id)  # Get the wardrobe item associated with this category

            # Append the wardrobe item details to favorite_items
            favorite_items.append({
                'f_id': fav.f_id,
                'image_name': wardrobe_item.image_name,
                'image_path': wardrobe_item.img_path.url,  # Assuming you want the URL for the image
                'category': category.Category,
                'color': category.Color,
                'occasion': category.Occassion,
            })
        # favorite_items = Favourites.objects.filter(user=request.user).select_related('c_id')
        return render(request, 'favourite.html', {'favorite_items': favorite_items})
    else:
        return redirect('login')



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


def add_to_favorites(request, category_id):
    # Ensure 'category_id' is valid
    category = get_object_or_404(Category, c_id=category_id)

    # Get the logged-in user instance
    user = request.user  # Assuming 'request.user' is set to the logged-in user instance

    # Retrieve the new_user instance associated with the logged-in user
    user_instance = get_object_or_404(new_user, username=user.username)

    # Create or get a favorite item entry
    favorite, created = Favourites.objects.get_or_create(u_id=user_instance, c_id=category)

    # Redirect or render a response after adding to favorites
    return redirect('favourite')


def remove_outfit(request, id):
    if request.method == 'POST':
        favorite_item = get_object_or_404(Favourites, f_id=id)
        favorite_item.delete()  # Remove the favorite item
        return redirect('favourite')
    
def remove_from_wardrobe(request,category_id):
    if request.method == 'POST':
        print("*********in remove wid************",category_id)
        Category_item = get_object_or_404(Category, c_id=category_id)
        print("*********in remove wid************",Category_item.w_id_id)
        wardrobe_item = get_object_or_404(Wardrobe, w_id=Category_item.w_id_id)
        wardrobe_item.delete()  # Remove the wardrobe_item item
        return redirect('view_wardrobe')

from django.shortcuts import render
from django.http import HttpResponse

# Define the quiz view
def quiz(request):
    return render(request, 'quiz.html')

# Define the result view
def result(request):
    if request.method == 'POST':
        # Collect answers from POST request
        answers = {
            'q1': request.POST.get('q1'),
            'q2': request.POST.get('q2'),
            'q3': request.POST.get('q3'),
            'q4': request.POST.get('q4'),
            'q5': request.POST.get('q5')
        }

        # Calculate the personality style based on answers
        style_scores = {
            'Casual': 0,
            'Formal': 0,
            'Bohemian': 0,
            'Minimalist': 0
        }

        # Assign scores based on answers
        for answer in answers.values():
            if answer == 'A':
                style_scores['Casual'] += 1
            elif answer == 'B':
                style_scores['Bohemian'] += 1
            elif answer == 'C':
                style_scores['Minimalist'] += 1
            elif answer == 'D':
                style_scores['Formal'] += 1

        # Determine the highest scoring style
        personality_type = max(style_scores, key=style_scores.get)

        # Return the result to the result page
        return render(request, 'result.html', {'personality_type': personality_type})
    
    return HttpResponse("No answers received.")
