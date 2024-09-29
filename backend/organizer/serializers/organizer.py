from organizer.models import Organizer
from rest_framework.serializers import ModelSerializer


class OrganizerSerializer(ModelSerializer):
    class Meta:
        model = Organizer
        fields = ["id", "email", "password", "company_name", "phone", "cnpj", "date_joined"]
        extra_kwargs = {"password": {"write_only": True}}
