from django.urls import path
from user_activity.views import UserActivityView

urlpatterns = [
    path('me', UserActivityView.as_view(), name='my_user_activity'),
]
