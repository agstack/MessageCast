from django.urls import path, include
from api.views import Register, Login, Logout, HomeView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', Login.as_view(), name='custom_login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='custom_logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]


urlpatterns += staticfiles_urlpatterns()
