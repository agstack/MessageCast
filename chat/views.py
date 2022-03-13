from django.shortcuts import render
from django.views.generic import TemplateView


class Chat(TemplateView):
    template_name = 'chat/index.html'

    def get(self, request):
        return render(request, self.template_name, {})


def room(request, room_name):

    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

