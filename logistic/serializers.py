from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'stocks']
    #
    # def create(self, validated_data):
    #     product = super().create(validated_data)
    #     return product
    #
    # def update(self, instance, validated_data):
    #     product = super().update(instance, validated_data)
    #     return product


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):

    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'products', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for pos in positions:
            StockProduct.objects.update_or_create(stock=stock, **pos)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for pos in positions:
            StockProduct.objects.update_or_create(stock=stock, product=pos['product'], defaults={'price': pos['price'],
                        'quantity': pos['quantity']
                        })
        return stock
