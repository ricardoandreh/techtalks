from organizer.serializers import OrganizerSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


class OrganizerRegisterView(CreateAPIView):
    serializer_class = OrganizerSerializer
    permission_classes = (AllowAny,)
