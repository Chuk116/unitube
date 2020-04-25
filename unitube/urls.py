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
from django.urls import path, include
from django.conf.urls import url
from onboard import views as onboard_views
from videos import views as videos_views
from account import views as account_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('edit-profile/', account_views.edit_profile, name="edit_profile"),
    path('my-profile/', account_views.my_profile, name="my_profile"),
    path('view-profile/<str:username>/', account_views.view_profile, name="view_profile"),
    # path('search/', videos_views.search, name="search-videos"),
    path('search/q=<str:query>/', videos_views.search, name="search-videos"),
    path('search/q=<str:query>/<int:s>/', videos_views.filter_search, name="filter-search"),
    path('post-video/', videos_views.post_video, name="post-video"),
    path('video-page/<str:video_id>/', videos_views.video_page, name="video-page"),
    path('post-comment/', videos_views.post_comment, name="post-comment"),
    path('post-rating/', videos_views.post_rating, name="post-rating"),

    path('', onboard_views.home, name="home"),
    path('logout', onboard_views.logout, name="logout"),
    path('login/', onboard_views.login, name="login"),
    path('signup/', onboard_views.signup, name="signup"),
    path('admin/', admin.site.urls),
    # path('cas/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    # path('cas/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
