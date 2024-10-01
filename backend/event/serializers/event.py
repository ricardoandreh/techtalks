from event.models import Event
from organizer.models import Organizer
from organizer.serializers import OrganizerSerializer
from rest_framework.serializers import (ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField)


class EventSerializer(ModelSerializer):
    organizer = PrimaryKeyRelatedField(queryset=Organizer.objects.all())
    organizer_detail = SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"
    
    def create(self, validated_data):
        organizer = validated_data.pop("organizer")
        event = Event.objects.create(organizer=organizer, **validated_data)
        return event

    def get_organizer_detail(self, obj):
        return OrganizerSerializer(obj.organizer).data
