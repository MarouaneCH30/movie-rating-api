from django.urls import path
from user_app.api.views import registration_view, login_view, logout_view

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # If you later switch to JWT (SimpleJWT):
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
