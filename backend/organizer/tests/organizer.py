from django.conf import settings
from django.urls import reverse
from organizer.models import Organizer
from organizer.serializers import OrganizerSerializer
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class OrganizerTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("token_obtain_pair")
        self.organizer_list_url = reverse("organizer-list")
        self.register_url = reverse("organizer-register")
        self.page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 10)

    def test_register_organizer(self):
        data = {
            "company_name": "Event Co.",
            "password": "strongpass123",
            "email": "event_co@example.com",
            "phone": "1234567890",
            "cnpj": "12.345.608/0001-90"
        }

        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organizer.objects.get().cnpj, "12.345.608/0001-90")
        self.assertEqual(Organizer.objects.get().company_name, "Event Co.")

    def test_login_organizer(self):
        Organizer.objects.create_user(
            company_name="organizer1",
            password="password123",
            email="organizer1@example.com",
            phone="1234567890",
            cnpj="14.345.678/0001-90"
        )

        data = {
            "email": "organizer1@example.com",
            "password": "password123"
        }

        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_get_organizers_data(self):
        Organizer.objects.create_user(
            company_name="IFC Meet",
            password="password123",
            email="meet@ifc.edu.br",
            phone="1234567890",
            cnpj="12.345.278/0001-90",
        )

        login_data = {
            "email": "meet@ifc.edu.br",
            "password": "password123"
        }

        login_response = self.client.post(self.login_url, login_data, format="json")
        token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.organizer_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_get_organizer_detail_data(self):
        organizer = Organizer.objects.create_user(
            company_name="Fusion Show",
            password="password123",
            email="show@fusion.uk",
            phone="7357795231",
            cnpj="84.343.285/0001-63",
        )

        login_data = {
            "email": "show@fusion.uk",
            "password": "password123"
        }

        login_response = self.client.post(self.login_url, login_data, format="json")
        token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.organizer_detail_url = reverse("organizer-detail", kwargs={"pk": organizer.pk})

        response = self.client.get(self.organizer_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company_name"], "Fusion Show")
        self.assertEqual(response.data["email"], "show@fusion.uk")
        self.assertEqual(response.data["phone"], "7357795231")
        self.assertEqual(response.data["cnpj"], "84.343.285/0001-63")

    def test_get_organizers_data_unauthenticated(self):
        response = self.client.get(self.organizer_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_organizer_invalid_data(self):
        data = {
            "company_name": "",
            "password": "123",
            "email": "invalid-email",
            "phone": "invalid-phone",
            "cnpj": "invalid-cnpj"
        }

        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data) # Error Detail
        self.assertNotIn("company_name", response.data)
        self.assertNotIn("password", response.data)
        self.assertNotIn("phone", response.data)
        self.assertNotIn("cnpj", response.data)

    def test_update_organizer(self):
        organizer = Organizer.objects.create_user(
            company_name="Fusion Show",
            password="password123",
            email="show@fusion.uk",
            phone="7357795231",
            cnpj="84.343.285/0001-63",
        )

        login_data = {
            "email": "show@fusion.uk",
            "password": "password123"
        }

        login_response = self.client.post(self.login_url, login_data, format="json")
        token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.organizer_detail_url = reverse("organizer-detail", kwargs={"pk": organizer.pk})

        update_data = {
            "company_name": "Fusion Show Updated",
            "phone": "9876543210"
        }

        response = self.client.patch(self.organizer_detail_url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company_name"], "Fusion Show Updated")
        self.assertEqual(response.data["phone"], "9876543210")

    def test_delete_organizer(self):
        organizer = Organizer.objects.create_user(
            company_name="Fusion Show",
            password="password123",
            email="show@fusion.uk",
            phone="7357795231",
            cnpj="84.343.285/0001-63",
        )

        login_data = {
            "email": "show@fusion.uk",
            "password": "password123"
        }

        login_response = self.client.post(self.login_url, login_data, format="json")
        token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.organizer_detail_url = reverse("organizer-detail", kwargs={"pk": organizer.pk})

        response = self.client.delete(self.organizer_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Organizer.objects.filter(pk=organizer.pk).exists())

    def test_serializer_validation(self):
        data = {
            "company_name": "Test Company",
            "password": "password123",
            "email": "test@example.com",
            "phone": "1234567890",
            "cnpj": "12.345.678/0001-90"
        }

        serializer = OrganizerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["company_name"], "Test Company")

    def test_search_organizers(self):
        Organizer.objects.create_user(
            company_name="Search Test",
            password="password123",
            email="search@test.com",
            phone="1234567890",
            cnpj="12.345.678/0001-90",
        )

        login_data = {
            "email": "search@test.com",
            "password": "password123"
        }

        login_response = self.client.post(self.login_url, login_data, format="json")
        token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.organizer_list_url, {"search": "Search Test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["company_name"], "Search Test")

    def test_get_organizers_with_pagination(self):
        for i in range(15):
            Organizer.objects.create_user(
                company_name=f"Organizer {i}",
                password="password123",
                email=f"organizer{i}@example.com",
                phone=f"123456789{i}",
                cnpj=f"12.345.678/000{i}-90",
            )

        login_data = {
            "email": "organizer0@example.com",
            "password": "password123"
        }

        login_response = self.client.post(self.login_url, login_data, format="json")
        token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.organizer_list_url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), self.page_size)
