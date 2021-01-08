from django.urls import path

from . import views

app_name = 'voting'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('genquestion', views.genquestion, name='genquestion'),
    path('<int:pk>/addtext', views.addtext, name='addtext'),
    path('<int:pk>/addchoice', views.addchoice, name='addchoice'),
    path('<int:pk>/new', views.new, name='new'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]