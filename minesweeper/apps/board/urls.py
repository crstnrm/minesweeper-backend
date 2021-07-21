from django.urls import path
from board import views

urlpatterns = [
    path('', views.BoardView.as_view()),
    path('<int:pk>/', views.BoardDetailView.as_view()),
    path('<int:pk>/inspect/', views.InspectBoardCellView.as_view()),
]
