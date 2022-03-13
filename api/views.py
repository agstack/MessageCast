from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.models import User, APIProduct, Subscription
from api.serializers import APIProductSerializer, SubscriptionSerializer
from api.utils import send_email
from chat.models import Chat
from chat.serializers import ChatSerializer


class Login(LoginView):
    login_url = '/login/'
    redirect_authenticated_user = True
    redirect_field_name = '/home/'


class Logout(LogoutView):
    next_page = '/login/'
    redirect_field_name = '/login/'


class Register(TemplateView):
    template_name = 'register.html'

    def get(self, request):
        return render(request, 'register.html', {})

    def post(self, request):

        # fetching geo-spatial data
        ip = request.META.get('REMOTE_ADDR')

        # username = email
        username = request.POST['username']
        phone = request.POST['phone']
        usage = request.POST['usage']
        password = request.POST['password']
        discoverable = True if request.POST.get('discoverable') == 'on' else False

        # typical registration protocol
        try:
            try:
                User.objects.get(email=username)
                return render(request, self.template_name, {'errors': 'Email already exists.'})
            except User.DoesNotExist:
                User.objects.create_user(username=username, password=password, email=username, ip=ip,
                                         phone=phone, usage=usage, discoverable=discoverable)
        except Exception as e:
            if str(e) == 'UNIQUE constraint failed: users_user.username':
                return render(request, self.template_name, {'errors': 'Username already taken.'})
            return render(request, self.template_name, {'errors': e})

        # send confirmation email
        # twilio integration

        return render(request, self.template_name, {'success': 'New User created', 'title': 'Register'})


class HomeView(TemplateView, LoginRequiredMixin, APIView):
    template_name = "home.html"
    login_url = '/login/'
    permission_classes = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # fetching all api product objects from database
        objs = APIProduct.objects.all()
        context['api_products'] = APIProductSerializer(objs, many=True).data

        # preparing context for template
        context['title'] = 'Home'
        return context


class ConfirmationPageView(TemplateView, APIView):
    template_name = "confirmation_page.html"
    permission_classes = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # fetching all api product objects from database
        objs = APIProduct.objects.all()
        context['api_products'] = APIProductSerializer(objs, many=True).data

        # preparing context for template
        context['title'] = 'ConfirmationPage'
        return context

    def get(self, request):
        # getting request parameters
        user = request.user
        prod_id = request.GET.get('product_id')
        room = request.GET.get('chat')
        obj_api_product = APIProduct.objects.filter(id=prod_id).first()

        # redirect to room
        if room:
            chat_objs = Chat.objects.filter(chat_room_id=prod_id).order_by('created_at')
            chat_messages = ChatSerializer(chat_objs, many=True).data
            return render(request, 'chat/room.html', {
                'room_name': obj_api_product.name,
                'chat_messages': [f"{cm['message']} - {cm['username']} - {cm['created_at']} - {cm['city']}, {cm['region']}, {cm['country']}" for cm in chat_messages]
            })

        # creating or fetching subscription object
        obj_subscription, created = Subscription.objects.get_or_create(user=user, api_product=obj_api_product)

        # preparing context for template
        context = {
            'product': APIProductSerializer(obj_api_product).data,
            'subscription': SubscriptionSerializer(obj_subscription).data,
            'title': 'ConfirmationPage',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # getting request parameters
        user = request.user
        prod_id = request.POST.get('product_id')
        # unsubscribe = request.POST.get('unsubscribe')
        subscribe = request.POST.get('subscribe')
        subscription = 'subscribed' if subscribe else 'unsubscribed'

        obj_api_product = APIProduct.objects.filter(id=prod_id).first()
        if obj_api_product is not None:
            # updating the subscription status
            obj_subscription, created = Subscription.objects.get_or_create(user=user, api_product=obj_api_product)
            obj_subscription.status = True if subscribe else False
            obj_subscription.save()

            # sending email notification of the subscription
            msg = f"Thanks for subscribing to {obj_api_product.name} from AgStack. Please note to use the following token in all your API queries. E.g., www.agstack.org/{obj_api_product.name}&lat=<lattitude>&lon=<longitude>&api_token={obj_subscription.token}. Please email any questions to support@agstack.org"
            send_email(msg, user)

        # preparing context for template
        context = {
            'title': 'ConfirmationPage',
            'product': APIProductSerializer(obj_api_product).data,
            'status': 'Your subscription status has been updated',
        }
        return render(request, self.template_name, context)
