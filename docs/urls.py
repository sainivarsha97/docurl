from django.contrib import admin
from django.conf.urls import url
from django.urls import path , include
from .views import DocumentView,ContentView,GeneratePDF,EditView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',DocumentView,name="document"),
    path('<username>', ContentView,name="content"),
    path('<username>/pdf', GeneratePDF,name="pdf"),
    path('<username>/edit', EditView,name="edit"),
]
urlpatterns+=staticfiles_urlpatterns()
