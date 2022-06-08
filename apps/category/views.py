from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from .models import Category
from .serializers import CategorySerializer
from .permissions import IsAdminOrAllowAny


class CategoryListCreateView(ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsAdminOrAllowAny,]