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
from Fashion.views import index,login_view,signup,upload,insights,map_view,view_donations,send_donation_request,generate_invoice,profile,aboutus
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path




urlpatterns = [
    path('get_organizations/', map_view, name='get_organizations'),
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('index/',index,name='index'),
    path('login/',login_view,name='login'),
    path('signup/',signup,name='signup'), 
    path('aboutus/',aboutus,name='aboutus'),
    path('upload/',upload,name='upload'),
    path('profile/',profile,name='profile'),
    path('index/',index,name='index'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('insights/', insights, name='insights'),
    path('view-donations/', view_donations, name='view_donations'),
    path('send_donation_request/', send_donation_request, name='send_donation_request'),
    path('generate_invoice/<int:donation_id>/', generate_invoice, name='generate_invoice'),
    # Other URL patterns
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
