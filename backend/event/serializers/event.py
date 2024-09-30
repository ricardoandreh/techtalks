from event.models import Event
from organizer.models import Organizer
from organizer.serializers import OrganizerSerializer
from rest_framework.serializers import ModelSerializer


class EventSerializer(ModelSerializer):
    organizer = OrganizerSerializer()

    class Meta:
        model = Event
        fields = "__all__"
    
    def create(self, validated_data):
        organizer_data = validated_data.pop("organizer")
        organizer, created = Organizer.objects.get_or_create(**organizer_data)
        event = Event.objects.create(organizer=organizer, **validated_data)
        
        return event
