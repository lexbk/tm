"""URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/

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
from django.http import HttpRequest, HttpResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse("API is running 🚀")


urlpatterns = [
    path('', home),

    path('admin/', admin.site.urls),

    path('api/v1/', include('app.urls')),

    # 1. This generates the raw schema file (Required)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # 2. Map the Swagger UI to your exact preferred '/docs/' path
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Optional: Map Redoc UI if you prefer that style instead
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
