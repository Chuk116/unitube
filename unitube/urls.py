"""unitube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from onboard import views as onboard_views
from posting import views as posting_views
from searching import views as search_views
from account import views as account_views
import cas.views
urlpatterns = [
    path('edit-profile/', account_views.edit_profile, name="edit_profile"),
    path('profile/', account_views.view_profile, name="view_profile"),
    
    path('search/', search_views.search, name="search-videos"),
    path('post-video/', posting_views.post_video, name="post-video"),
    
    # CAS
    path('admin/login/', cas.views.login, name='login'),
    path('admin/logout/', cas.views.logout, name='logout'),
    path('', onboard_views.login, name="home"),
    path('logout', onboard_views.logout, name="logout"),
    path('login/', onboard_views.login, name="login"),
    path('signup/', onboard_views.signup, name="signup"),
    path('admin/', admin.site.urls),
]
