# django packages
from django.db.models import Q
from django.http import Http404
# django rest framework packages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# local packages
from apps.adopcion.models import Persona
from apps.adopcion.serializers import PersonaSerializer, EditPersonaSerializer


class PersonaList(APIView):
    def get(self, request):
        queryset = Persona.objects.all()
        search_query = request.query_params.get('q')
        if search_query:
            args = [Q(nombre__contains=search_query) | Q(apellidos__contains=search_query) |
                    Q(email__contains=search_query)]
            queryset = queryset.filter(*args)
        serializer = PersonaSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EditPersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PersonaDetail(APIView):
    def get_object(self, pk):
        try:
            return Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        entity = self.get_object(pk)
        serializer = PersonaSerializer(entity)
        return Response(serializer.data)

    def put(self, request, pk):
        entity = self.get_object(pk)
        serializer = EditPersonaSerializer(entity, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        entity = self.get_object(pk)
        entity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
