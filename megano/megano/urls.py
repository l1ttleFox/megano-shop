"""
URL configuration for megano project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sign-in", RedirectView.as_view(url="sign-in/", permanent=True)),
    path("sign-up", RedirectView.as_view(url="sign-up/", permanent=True)),
    path("profile", RedirectView.as_view(url="profile/", permanent=True)),
    path("sale", RedirectView.as_view(url="sale/", permanent=True)),
    path("catalog", RedirectView.as_view(url="catalog/", permanent=True)),
    path("", include("frontend.urls")),
    path("api/", include("authapp.urls")),
    path("api/", include("productapp.urls")),
    path("api/", include("orderapp.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
