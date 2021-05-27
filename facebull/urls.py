from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('publish', views.Publish.as_view(), name='publish'),
    path('access/<int:pk>', views.AccessPost.as_view(), name='access'),
    path('like/<post_id>', views.LikePost.as_view(), name='like'),
    path('unlike/<post_id>', views.UnlikePost.as_view(), name='unlike'),
]