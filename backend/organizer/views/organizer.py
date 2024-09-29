from organizer.models import Organizer
from organizer.serializers import OrganizerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class OrganizerViewSet(ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = (IsAuthenticated,)
