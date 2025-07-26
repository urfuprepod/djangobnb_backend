from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Conversation
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from useraccount.models import User

@api_view(['GET'])
def conversation_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(), many = True)
    
    return JsonResponse({'data': serializer.data})


@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = request.user.conversations.get(pk = pk)
    
    conversation_serializer = ConversationDetailSerializer(conversation, many = False)
    messages_serializer = ConversationMessageSerializer(conversation.message.all(), many = True)
    
    return JsonResponse({
        'conversation': conversation_serializer.data,
        'messages': messages_serializer.data,
    },)
    
@api_view(['GET'])
def conversation_start(request, user_id):
    conversations = Conversation.objects.filter(user__in=[user_id]).filter(users__in=[request.user.id])
    
    if conversations.count() > 0:
        conversation = conversations.first()
        return JsonResponse({
            'data': conversation.id
        })
    user = User.objects.get(pk = user_id)
    conversation = Conversation.objects.create()
    conversation.users.add(request.user)
    conversation.users.add(user)
    return JsonResponse({
        'data': conversation.id
    })