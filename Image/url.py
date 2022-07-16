from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.exceptions import *
from django.urls import path
from Image import views
from django.shortcuts import HttpResponse

app_name = "image"
try:
    urlpatterns = [
        path('add', views.addImage, name="add_image"),
        path('dashboard', views.dashboard, name="dashboard"),
        path('detail/<int:id>', views.detail, name="detail"),
        path('update/<int:id>', views.updateImages, name="update"),
        path('delete/<int:id>', views.deleteImage, name="delete"),
        path('image/', views.images, name="image_detail"),
    ]
    if settings.DEBUG:  # Dev only
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
except ViewDoesNotExist:
    print("The View does not exist in views.py")

