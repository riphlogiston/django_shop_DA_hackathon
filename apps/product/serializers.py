from rest_framework import serializers

from .models import Product, Review

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=('id', 'title', 'price', 'image', 'watch')
    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['author']=instance.author.email
        representation['category']=instance.category.title
        representation['reviews']=instance.reviews.all().count()
        return representation

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        exclude=("author",)

    def validate(self,attrs):
        request=self.context.get('request')
        attrs['author']=request.user
        return attrs
    
    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['author']=instance.author.email
        representation['category']=instance.category.title
        representation['reviews']=ReviewSerializer(instance.reviews.all(), many=True).data
        representation['likes']=instance.likes.filter(is_liked=True).count()
        representation['favs']=instance.favourites.filter(favourite=True).count()
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        exclude=("author",)
    
    def validate(self,attrs):
        request=self.context.get('request')
        attrs['author']=request.user
        return attrs
    
    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['author']=instance.author.email
        representation['product']=instance.product.title
        return representation

class FavouriteSerializer(serializers.ModelSerializer):
    class  Meta:
        model=Product
        fields='__all__'
    





