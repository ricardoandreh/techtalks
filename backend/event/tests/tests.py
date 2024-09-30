from django.conf import settings
from django.urls import reverse
from event.models import Event
from organizer.models import Organizer
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class EventTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.event_list_url = reverse("event-list")
        self.page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 10)
        
        self.organizer = Organizer.objects.create(
            company_name="Tech Corp",
            email="contact@techcorp.com",
            phone="1234567890",
            cnpj="12.345.678/0001-99"
        )
        
        Event.objects.create(
            title="Tech Conference",
            description="Annual tech conference.",
            date="2024-09-29T13:00:00Z",
            is_remote=True,
            event_url="http://example.com/event",
            organizer=self.organizer
        )

    def test_get_all_events(self):
        response = self.client.get(self.event_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_event(self):
        data = {
            "title": "New Event",
            "description": "This is a new event.",
            "date": "2024-10-01T13:00:00Z",
            "is_remote": False,
            "event_url": "http://example.com/new_event",
            "organizer": {
                "company_name": "New Tech Corp",
                "password": "strongpass123",
                "email": "newcontact@techcorp.com",
                "phone": "0987654321",
                "cnpj": "98.765.432/0001-99"
            }
        }

        response = self.client.post(self.event_list_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Event.objects.get(id=2).title, "New Event")

    def test_create_event_missing_fields(self):
        data = {
            "title": "Incomplete Event",
            "description": "This event is missing some fields.",
            # Missing date and organizer properties
        }

        response = self.client.post(self.event_list_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)
        self.assertIn("organizer", response.data)

    def test_create_event_invalid_date(self):
        data = {
            "title": "Invalid Date Event",
            "description": "This event has an invalid date.",
            "date": "invalid-date",
            "is_remote": False,
            "event_url": "http://example.com/invalid_date_event",
            "organizer": {
                "company_name": "Invalid Date Corp",
                "password": "strongpass123",
                "email": "invaliddate@corp.com",
                "phone": "0987654321",
                "cnpj": "98.765.432/0001-99"
            }
        }

        response = self.client.post(self.event_list_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)

    def test_pagination(self):
        for i in range(self.page_size + 1):
            Event.objects.create(
                title=f"Event {i}",
                description=f"Description for event {i}",
                date="2024-10-01T13:00:00Z",
                is_remote=False,
                event_url=f"http://example.com/event_{i}",
                organizer=self.organizer
            )

        response = self.client.get(self.event_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), self.page_size)
        self.assertIn("next", response.data)
        self.assertIsNotNone(response.data["next"])