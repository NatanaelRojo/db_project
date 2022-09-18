from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('poll_detail/<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('question_detail/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<int:pk>/results/', views.QuestionResultView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]