from django.urls import path

from . import views

urlpatterns = [
    path('all_authors/', views.AllAuthorsApiView.as_view()),
]
