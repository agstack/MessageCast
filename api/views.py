from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from AgStackRegistry.local_settings import EMAIL_HOST_USER, BASE_URL
from api.models import User, APIProduct, Subscription
from api.serializers import APIProductSerializer, SubscriptionSerializer
from api.utils import send_email
from chat.models import Message, Tag
from chat.serializers import MessageSerializer, TagSerializer


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

    def invite_user_text(self, user, obj_api_product, user_invite_obj):
        url = BASE_URL + 'confirmation_page/?product_id=1&chat=chat&invite_email='
        msg = f"Hi {user_invite_obj.first_name},\n\n" \
              f"This is {user.get_full_name()}. There is a topic called '{obj_api_product.name}' " \
              f"on AgStack chat that I think you'll find interesting! Click on the link below to join. " \
              f"See you there!\n\n" \
              f"{url}\n\n" \
              f"Best Regards,\n" \
              f"{user.first_name}\n"

        email_text = """Subject: %s

%s
        """ % ('Interesting topic on AgStack chat!', msg)

        return email_text

    def invite_to_agstack_text(self, user, user_invite_obj):
        url = BASE_URL + 'register'
        msg = f"Hi {user_invite_obj.first_name},\n\n" \
              f"This is {user.get_full_name()}. I would like to invite you to join AgStack, an open-source digital " \
              f"infrastructure for the agriculture ecosystem! AgStack is a Linux Foundation project launched in " \
              f"2021 to help improve global agriculture efficiency through the creation, maintenance and enhancement " \
              f"of free, reusable, open and specialized digital infrastructure for data and applications. You can " \
              f"learn more about AgStack at " \
              f"{url}\n\n" \
              f"Best Regards,\n" \
              f"{user.first_name}\n"

        email_text = """Subject: %s

%s
        """ % ('Invitation to join AgStack, an Open-Source Digital Infrastructure for the Agriculture Ecosystem!', msg)

        return email_text

    def update_tags_list(self, d):
        return {'tag': d['tag']}

    def get(self, request):
        # getting request parameters
        user = request.user
        prod_id = request.GET.get('product_id')
        room = request.GET.get('chat')
        invite = request.GET.get('invite')
        obj_api_product = APIProduct.objects.filter(id=prod_id).first()

        # invite email user
        if invite:
            invite_email = request.GET.get('invite_email')
            user_invite_obj = User.objects.filter(email=invite_email).first()
            if user_invite_obj:
                # email user if email exists
                email_text = self.invite_user_text(user, obj_api_product, user_invite_obj)
                send_email(email_text, user_invite_obj)
                objs = APIProduct.objects.all()
                return render(request, 'home.html', {
                    'success': 'user invited via email',
                    'api_products': APIProductSerializer(objs, many=True).data
                })
            else:
                email_text = self.invite_to_agstack_text(user, user_invite_obj)
                send_email(email_text, user_invite_obj)
                objs = APIProduct.objects.all()
                return render(request, 'home.html', {
                    'error': 'user doesn’t exist',
                    'api_products': APIProductSerializer(objs, many=True).data
                })

        # redirect to room
        if room:
            chat_objs = Message.objects.filter(topic_id=prod_id).order_by('created_at')
            chat_messages = MessageSerializer(chat_objs, many=True).data
            # chat_messages = [[message1, upvote1, downvote1], [message2, upvote2, downvote2], ....]
            msgs = []
            for cm in chat_messages:
                temp_msg = []
                temp_msg.append(cm['id'])
                temp_msg.append(f"{cm['description']} - {cm['username']} - {cm['created_at']} - {cm['city']}, {cm['region']}, {cm['country']}")
                temp_msg.append(cm['upvote'])
                temp_msg.append(cm['downvote'])
                if cm['file']:
                    temp_msg.append(cm['file'])
                else:
                    temp_msg.append('')
                msgs.append(temp_msg)

            tag_objs = Tag.objects.all()

            tags_serialized = TagSerializer(tag_objs, many=True).data

            tags = list(map(self.update_tags_list, tags_serialized))

            return render(request, 'chat/room.html', {
                'room_name': obj_api_product.name,
                'chat_messages': msgs,
                'tags': tags
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


class ManageVoting(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        chat_id = request.data.get('chat_id')
        voting_type = request.data.get('voting_type')
        msg_obj = Message.objects.filter(id=chat_id).order_by('created_at').first()

        if (user not in msg_obj.upvoters.all()) and (user not in msg_obj.downvoters.all()):
            if voting_type == 'upvote':
                msg_obj.upvote += 1
                msg_obj.upvoters.add(self.request.user)
                msg_obj.save()
                return Response({'status': True})
            elif voting_type == 'downvote':
                msg_obj.downvote += 1
                msg_obj.downvoters.add(self.request.user)
                msg_obj.save()
                return Response({'status': True})

        return Response({'status': False})


def home_test(request):
    languages = Tag.objects.all()
    return render(request,'test.html',{"languages":languages})
