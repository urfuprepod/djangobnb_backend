from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationListSerializer
from .forms import PropertyForm
from useraccount.models import User
from rest_framework_simplejwt.tokens import AccessToken

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    
    try:
        token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
        token = AccessToken(token)
        user_id = token.payload['user_id']
        user = User.objects.get(pk = user_id)
    except Exception as e:
        user = None
    
    properties = Property.objects.all()
    serializer = PropertiesListSerializer(properties, many=True)
    
    is_favorites = request.GET.get('is_favorites', '')
    landlord_id = request.GET.get('landlord_id', '')
    if landlord_id:
        properties = properties.filter(landlord_id = landlord_id)
        
    if is_favorites == 'true':
        properties = properties.filter(favorited__in=[user])
    favorites = []
    if user:
        for property in properties:
            if user in property.favorited.all():
                favorites.append(property.id)
    return JsonResponse({
        'data': serializer.data,
        'favorites': favorites
    })
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk = pk)
    
    
    
    serializer = PropertiesDetailSerializer(property, many = False)
    
    return JsonResponse(serializer.data)
    
    
@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()
        
        return JsonResponse({'success': True}, status = 201)
    return JsonResponse({'errors': form.errors.as_json()}, status=400)

@api_view(['POST'])
def book_property(request, pk):
    try: 
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')
        
        property = Property.objects.get(pk=pk)
        
        Reservation.objects.create(property = property, start_date=start_date, end_date=end_date, number_of_nights=number_of_nights, total_price=total_price, guests=guests, created_by=request.user)
        return JsonResponse({'success': True})
    except Exception as e:
        print('Error', e)
        return JsonResponse({'success': False})
    
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    property = Property.objects.get(pk = pk)
    resevations = property.reservations.all()
    
    serializer = ReservationListSerializer(resevations, many = True)
    
    return JsonResponse({
        'data': serializer.data
    })
    
    
@api_view(['POST'])
def toggle_favorite(request, pk):
    property = Property.objects.get(pk=pk)
    
    if request.user in property.favorited.all():
        property.favorited.remove(request.user)
        return JsonResponse({'is_favorited': False})
    
    property.favorited.add(request.user)
    return JsonResponse({'is_favorited': True})