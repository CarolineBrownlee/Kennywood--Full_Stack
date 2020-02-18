"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import ParkArea


class ParkAreaSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = ParkArea
        url = serializers.HyperlinkedIdentityField(
            view_name='parkarea',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'theme')

# The ViewSet class allows you to write logic for the operations that can be performed on a resource in the API. The first operations you will handle are a client requesting one park area, and a request for all park areas. For these operations, the ViewSet exposes retrieve() and list() methods. Your logic goes in those methods. (Nashville Software School, Chapter Docs)
class ParkAreas(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            area = ParkArea.objects.get(pk=pk)
            serializer = ParkAreaSerializer(area, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        # It's an abstraction that the Object Relational Mapper (ORM) in Django provides that queries the table holding all the park areas, and returns every row. It is the equivalent of you explicitly writing the following SQL. (Nashville Software School, Chapter Docs)
        areas = ParkArea.objects.all()
        serializer = ParkAreaSerializer(
            areas,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)