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
    
    country = request.GET.get('country', '')
    category=request.GET.get('category', '')
    guests= request.GET.get('numbGuests', '')
    bedrooms= request.GET.get('bedrooms', '')
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    
    if landlord_id:
        properties = properties.filter(landlord_id = landlord_id)
        
    if is_favorites == 'true':
        properties = properties.filter(favorited__in=[user])
        
    if guests:
        properties = properties.filter(guests__gte=guests)
        
    if bedrooms:
        properties = properties.filter(bedrooms__gte=guests)
    
    if country:
        properties = properties.filter(country=country)
    
    if category:
        properties = properties.filter(category=category)
        
    if checkin and checkout:
        exact_matches = Reservation.objects.filter(start_date=checkin) | Reservation.objects.filter(end_date=checkout)
        overlap_matches = Reservation.objects.filter(start_date__lte=checkout, end_date__gte=checkin)
        all_matches = []
        
        for reservation in exact_matches, overlap_matches:
            all_matches.append(reservation.property_id)
        properties = properties.exclude(id__in=all_matches)
    
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