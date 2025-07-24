from .serializers import UserDetailSeralizer
from .models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from property.serializers import ReservationListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def landlord_detail(request, pk):
    user = User.objects.get(pk = pk)
    serializer = UserDetailSeralizer(user)
    
    return JsonResponse({
        'data': serializer.data
    })
    
    
@api_view(['GET'])
def reservations_list(request):
    reservations = request.user.reservations.all()
    serializer = ReservationListSerializer(reservations, many = True)
    
    return JsonResponse({
        'data': serializer.data
    })