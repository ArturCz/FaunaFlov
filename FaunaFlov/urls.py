"""
URL configuration for FaunaFlov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from myapp.views import (
Login_page,
Main_Page,
Add_Palnt,
Notifications,
My_plants,
Plant_details,
Logout

)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login_page.as_view(), name='login'),
    path('add_plant/', Add_Palnt.as_view(), name='add_plant'),
    path('notifications/', Notifications.as_view(), name='notifications'),
    path('my_plants/', My_plants.as_view(), name='my_plants'),
    path('main/', Main_Page.as_view(), name='main'),
    path('details/<int:pk>/', Plant_details.as_view(), name='plant_details'),
    path('my-plants/<int:pk>/water/', My_plants.as_view(), name='water_plant'),
    path('logout/', Logout.as_view(), name='logout')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)