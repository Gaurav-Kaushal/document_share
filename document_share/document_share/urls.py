"""document_share URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from authentication import views
from document_share.views import home
from share import views as share_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^upload/$', share_views.simple_upload, name='upload'),
    url(r'^logout/$', views.logout_view, name="log_out"),
    path('', home, name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

