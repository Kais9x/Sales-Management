from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.urls import path

from django.contrib import admin
from . import views
from django.urls import re_path
from django.views.static import serve


urlpatterns = [
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("test", views.test, name="index"),
    path("warehouses", views.warehouses, name="warehouses"),
    path('api/', include('sales.apis')),
    path("admin/", admin.site.urls),
]


urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

urlpatterns += [
  re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
  re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
