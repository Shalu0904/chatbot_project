from django.urls import path
from . import views

urlpatterns = [
    path('', views.unified_view, name='upload_pdf'),
    #path('summarize/', views.summarize, name='summarize'),
    #path('answer_question/', views.answer_question, name='answer_question'),
]
