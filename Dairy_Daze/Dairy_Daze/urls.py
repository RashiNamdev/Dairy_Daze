"""
URL configuration for Dairy_Daze project.

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
from django.urls import path

#from .views import home  # Import home view

urlpatterns = [
    path('admin/', admin.site.urls),
]


from django.contrib import admin
from django.urls import path, include
from authentication.views import front_page
urlpatterns = [

    # path('', home, name='home'),  # Default homepage
   
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),  # ← Replace `your_app` with your actual app name
    path('', front_page, name= 'registration'),
]
