from django.urls import path, include
from api.views import Register, Login, Logout, HomeView, ConfirmationPageView, ManageVoting, home_test, APIProductView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('voting/', ManageVoting.as_view(), name='voting'),
    path('confirmation_page/', ConfirmationPageView.as_view(), name='confirmation_page'),
    path('login/', Login.as_view(), name='custom_login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='custom_logout'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search/', APIProductView.as_view({'get': 'list'})),

]


urlpatterns += staticfiles_urlpatterns()
