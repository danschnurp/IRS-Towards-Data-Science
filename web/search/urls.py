from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path('', views.index, name='index'),
    path('question_search/', views.question_search, name="question_search"),
    path('question_search/<int:page>/', views.question_search_pagination, name="question_search_pagination"),
    path('api/question_search/', views.question_search_content_loader, name="question_search_content_loader"),
    path('api/question_search/<int:page>/', views.question_search_content_loader, name="question_search_content_loader"),
    path('explore_questions/', views.explore_questions, name="explore_questions"),
    path('explore_questions/<int:page>/', views.explore_questions_pagination, name="explore_questions_pagination"),
    path('api/explore_questions/', views.explore_questions_content_loader, name="explore_questions_content_loader"),
    path('api/explore_questions/<int:page>/', views.explore_questions_content_loader, name="explore_questions_content_loader"),
    path('detail/<str:page>/<int:post_id>/', views.detail, name="detail"),

]
