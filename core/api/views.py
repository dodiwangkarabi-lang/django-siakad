from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


class HealthCheckViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def health_check(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)