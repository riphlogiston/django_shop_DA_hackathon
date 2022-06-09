from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer
from apps.cart.models import ShoppingCart
from .services.utils import send_order_confirmation


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(shopping_cart__user=user)
    
    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated()]
        return[IsAdminUser()]
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        order=ShoppingCart.objects.filter(user=user)[0].cart_item.all()
        send_order_confirmation(user.email)
        order.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


        



    
    

