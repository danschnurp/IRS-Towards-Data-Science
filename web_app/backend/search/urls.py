from django.urls import path


from django.views.generic.base import TemplateView

from . import views
from .views import get_data

app_name = "search"
urlpatterns = [
    path('', views.index, name='index'),
    path('indexer/', views.indexer, name="index_manager"),
]
