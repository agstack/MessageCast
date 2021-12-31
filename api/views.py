from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from api.models import User


class Login(LoginView):
    login_url = '/login/'
    redirect_field_name = '/home/'


class Logout(LogoutView):
    next_page = '/login/'
    redirect_field_name = '/login/'


class Register(TemplateView):
    template_name = 'register.html'

    def get(self, request):
        return render(request, 'register.html', {})

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        usage = request.POST['usage']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        password = request.POST['password']

        # send confirmation email
        # twilio integration


        try:
            try:
                User.objects.get(email=email)
                return render(request, self.template_name, {'errors': 'Email already exists.'})
            except User.DoesNotExist:
                User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            if str(e) == 'UNIQUE constraint failed: users_user.username':
                return render(request, self.template_name, {'errors': 'Username already taken.'})
            return render(request, self.template_name, {'errors': e})
        else:
            return render(request, self.template_name, {'errors': 'Passwords do not match.'})

        return render(request, self.template_name, {'success': 'New User created'})


class HomeView(TemplateView, LoginRequiredMixin, View):
    template_name = "home.html"
    login_url = '/login/'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

        # context['plants'] = PlantsSerializer(Plant.objects.all().order_by('-created_at'), many=True).data
        # return context