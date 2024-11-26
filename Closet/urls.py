"""
URL configuration for Closet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Fashion.views import index,login_view,signup,aboutus,upload,profile,recommendation,view_wardrobe,insights,favourite,add_to_favorites, remove_outfit, remove_from_wardrobe,quiz,result
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('index/',index,name='index'),
    path('login/',login_view,name='login'),
    path('signup/',signup,name='signup'), 
    path('aboutus/',aboutus,name='aboutus'),
    path('upload/',upload,name='upload'),
    
    path('profile/',profile,name='profile'),
    path('recommendation/',recommendation,name='recommendation'),
    path('view_wardrobe/', view_wardrobe, name='view_wardrobe'),
    path('insights/', insights, name='insights'),
    path('favourite/', favourite, name='favourite'), 
    path('add_to_favorites/<uuid:category_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_wardrobe/<uuid:category_id>/', remove_from_wardrobe, name='remove_from_wardrobe'),
    path('remove_outfit/<uuid:id>/', remove_outfit, name='remove_outfit'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('favourite/', favourite, name='favourite'),
    path('quiz/', quiz, name='quiz'),  # Path for the quiz page
    path('result/', result, name='result'),
    # Other URL patterns
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
