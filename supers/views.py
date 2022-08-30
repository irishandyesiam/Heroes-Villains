from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from .models import Super
from supers import serializers
from .models import SuperType

@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':
        select_type = request.query_params.get('type')
        supers = Super.objects.all()
        if select_type:
            supers = supers.filter(super_type__type=select_type)
        serializer = SuperSerializer(supers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)   
    else:
        super_types = Super.objects.all()
        custom_response_dictionary = {}
        for super_type in super_types:
            supers = SuperType.objects.filter(super_type_id=super_type.id)
            serializer = SuperSerializer(supers, many=True)
            custom_response_dictionary[super_type.type] = {
                "heroes": serializer.type,
                "villians": serializer.type
            }
        return Response(custom_response_dictionary, status=status.HTTP_200_OK)
@api_view(['GET', 'PUT', 'DELETE'])
def super_detail(request, pk):
    super = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(super)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    elif request.method == 'PUT':
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)