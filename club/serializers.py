from rest_framework import serializers
from .models import User,Restos,Products,Bookings, BookingProduct



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

class BookingsSerializer(serializers.ModelSerializer):
    product_list = BookingProductSerializer(many=True)

    class Meta:
        model = Bookings
        fields = ['uid', 'resto_id', 'product_list']

    def create(self, validated_data):
        product_list_data = validated_data.pop('product_list')
        booking = Bookings.objects.create(**validated_data)

        for product_data in product_list_data:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity')

            try:
                product = Products.objects.get(product_id=product_id)
                BookingProduct.objects.create(booking=booking, product=product, quantity=quantity)
            except Products.DoesNotExist:
                pass

        return booking

