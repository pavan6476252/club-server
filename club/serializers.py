from rest_framework import serializers
from .models import User,Restos,Products

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class RestosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restos
        fields = '__all__'
class BookingSerializer(serializers.Serializer):
    resto_uuid = serializers.UUIDField()
    user_uuid = serializers.UUIDField()

    def validate(self, data):
        resto_uuid = data.get('resto_uuid')
        user_uuid = data.get('user_uuid')

        # Perform additional validations here
        # Example: Check if the user has the required permissions
        user = User.objects.filter(uid=user_uuid).first()
        if not user:
            raise serializers.ValidationError("Invalid user UUID.")
        
        if not user.has_permission('book_restaurant'):
            raise serializers.ValidationError("User does not have permission to book a restaurant.")

        # You can add more validations based on your requirements

        return data
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
