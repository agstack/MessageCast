from django.urls import path, include
from api.views import Login, Register, Logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('login/', Login.as_view(), name='custom_login'),
    path('register/', Register.as_view(), name='register'),
    # path('logout/', Logout.as_view(), name='custom_logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]


urlpatterns += staticfiles_urlpatterns()
