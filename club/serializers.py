from rest_framework import serializers
from .models import User,Restos,Products,Bookings, BookingProduct

import uuid

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


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'



class BookingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingProduct
        fields = ['product_id', 'quantity']

class BookingsSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    resto_id = serializers.PrimaryKeyRelatedField(queryset=Restos.objects.all())
    product_list = serializers.ListField(child=serializers.DictField(child=serializers.IntegerField()))

    def create(self, validated_data):
        uid = validated_data['uid']
        resto_id = validated_data['resto_id']
        product_list = validated_data['product_list']

        try:
            user = User.objects.get(uuid=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError({'uid': 'Invalid uid.'})
        except Restos.DoesNotExist:
            raise serializers.ValidationError({'resto_id': 'Invalid resto_id.'})

        booking = Bookings.objects.create(uid=user, resto_id=resto_id)
        for product_data in product_list:
            product_id = product_data.get('product')
            quantity = product_data.get('quantity')
            if product_id is not None and quantity is not None:
                try:
                    product = Products.objects.get(pk=product_id)
                except Products.DoesNotExist:
                    raise serializers.ValidationError({'product_id': f"Invalid product_id: {product_id}"})

                BookingProduct.objects.create(booking=booking, product=product, quantity=quantity)

        return booking
