from django.urls import path
from .views import TodoListCreate, TodoDetail,TodoToggleComplete

urlpatterns = [
    path('todos/', TodoListCreate.as_view(),),
    path('todos/<int:pk>/', TodoDetail.as_view(),),
    path('todos/<int:pk>/complete/', TodoToggleComplete.as_view(),),
]
