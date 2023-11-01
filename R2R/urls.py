"""
URL configuration for R2R project.

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
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'homepage.views.custom_page_not_found_view'
handler500 = 'homepage.views.custom_error_view'
handler403 = 'homepage.views.custom_permission_denied_view'
handler400 = 'homepage.views.custom_bad_request_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', LoginView.as_view(template_name="auth/login.html"), name="login" )

]
admin.site.site_title = "Reconnect to Rest site admin (R2R)"
admin.site.site_header = "R2R administration Dashboard"
admin.site.index_title = "R2R administration"

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
