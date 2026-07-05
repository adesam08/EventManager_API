from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Organizer, Event, Ticket,  Booking


User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['email'], email=validated_data['email'], password=validated_data['password'], first_name=validated_data['first_name'], last_name = validated_data['last_name'])
        return user
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class OrganizerUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    websites = serializers.URLField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        organizer = Organizer.objects.create(
            user=user,
            company_name=validated_data.get('company_name', ''),
            bio=validated_data.get('bio', ''),
            websites=validated_data.get('websites', ''),
        )
        return organizer

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.user.email,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'company_name': instance.company_name,
            'bio': instance.bio,
            'websites': instance.websites,
        }

class CreateEventSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'start_time',
            'end_time',
            
        ]
        

class TicketSerializer(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = [
                'event',
                'name',
                'price',
                'quantity_available'
            ]


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'location',
            'start_time',
            'end_time',
            'tickets',
            'organizer',
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'ticket',
            'quantity',
        ]
        









        
    