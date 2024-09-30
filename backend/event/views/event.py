from event.models import Event
from event.serializers import EventSerializer
from rest_framework.viewsets import ModelViewSet


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
