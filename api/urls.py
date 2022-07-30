from django.urls import path, include
from api.views import Register, Login, Logout, HomeView, ConfirmationPageView, ManageVoting, home_test, APIProductView, \
    ChatMessageView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import csrf_exempt

app_name = 'api'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('voting/', ManageVoting.as_view(), name='voting'),
    path(r'confirmation_page/', csrf_exempt(ConfirmationPageView.as_view()), name='confirmation_page'),
    path('login/', Login.as_view(), name='custom_login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='custom_logout'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search/', APIProductView.as_view({'get': 'list'}), name='search'),
    path('search-chat/', ChatMessageView.as_view({'get': 'list'}), name='search-chat'),
]


urlpatterns += staticfiles_urlpatterns()
