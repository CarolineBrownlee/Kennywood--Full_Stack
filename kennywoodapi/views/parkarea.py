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

    # Method that handles creating a single park
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """
        newarea = ParkArea()
        newarea.name = request.data["name"]
        newarea.theme = request.data["theme"]
        newarea.save()

        serializer = ParkAreaSerializer(newarea, context={'request': request})

        return Response(serializer.data)

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

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        area = ParkArea.objects.get(pk=pk)
        area.name = request.data["name"]
        area.theme = request.data["theme"]
        area.save()

        # The HTTP 204 No Content success status response code indicates that the request has succeeded, but that the client doesn't need to go away from its current page. (MDN Docs)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park area

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            area = ParkArea.objects.get(pk=pk)
            area.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ParkArea.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        # The Object Relational Mapper (ORM) that Django provides that queries the table holding all the park areas and returns every row. It is the equivalent of you explicitly writing SQL. (Nashville Software School, Chapter Docs)
        areas = ParkArea.objects.all()
        serializer = ParkAreaSerializer(
            areas,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)