from django.urls import path
from .views import UserCreateView, UserListView, UserRetrieveView, UserUpdateView, UserDeleteView

app_name = 'user'

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('list/', UserListView.as_view(), name='list_user'),
    path('detail/<str:pk>/', UserRetrieveView.as_view(), name='retrieve_user'),
    path('update/<str:pk>/', UserUpdateView.as_view(), name='update_user'),
    path('delete/<str:pk>/', UserDeleteView.as_view(), name='delete_user'),
]