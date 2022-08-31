from django.urls import path
from .views import TodoListCreate, TodoDetail, TodoToggleComplete, signup, login

urlpatterns = [
    path('todos/', TodoListCreate.as_view(),),
    path('todos/<int:pk>/', TodoDetail.as_view(),),
    path('todos/<int:pk>/complete/', TodoToggleComplete.as_view(),),
    path('signup/', signup),
    path('login/', login),
]
