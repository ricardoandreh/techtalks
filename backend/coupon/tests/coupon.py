from coupon.models import Coupon
from django.urls import reverse
from event.models import Event
from organizer.models import Organizer
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class CouponTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("token_obtain_pair")
        self.coupon_list_url = reverse("coupon-list")
        
        self.organizer = Organizer.objects.create_user(
            email="organizer@example.com", 
            password="password",
            company_name="Organizer Company"
        )
        self.other_organizer = Organizer.objects.create_user(
            email="other_organizer@example.com", 
            password="password",
            company_name="Other Organizer Company"
        )
        self.event = Event.objects.create(
            title="TechTalk",
            description="A tech event",
            date="2024-10-01T10:00:00Z",
            is_remote=True,
            organizer=self.organizer
        )
        self.other_event = Event.objects.create(
            title="Other Event",
            description="Another tech event",
            date="2024-11-01T10:00:00Z",
            is_remote=True,
            organizer=self.other_organizer
        )

        login_data = {
            "email": "organizer@example.com",
            "password": "password"
        }

        login_response = self.client.post(self.login_url, login_data, format="json")
        token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_coupon_for_own_event(self):
        data = {
            "discount": "10.00",
            "code": "DISCOUNT10",
            "valid": True,
            "event": self.event.id
        }
        
        response = self.client.post(self.coupon_list_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code"], "DISCOUNT10")

    def test_create_coupon_for_other_event(self):
        data = {
            "discount": "10.00",
            "code": "DISCOUNT10",
            "valid": True,
            "event": self.other_event.id
        }

        response = self.client.post(self.coupon_list_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_own_coupons(self):
        Coupon.objects.create(
            discount="10.00",
            code="DISCOUNT10",
            valid=True,
            event=self.event
        )

        response = self.client.get(self.coupon_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(response.data.get("results")[0].get("code"), "DISCOUNT10")

    def test_get_other_coupons(self):
        Coupon.objects.create(
            discount="10.00",
            code="DISCOUNT10",
            valid=True,
            event=self.other_event
        )

        response = self.client.get(self.coupon_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)

    def test_check_coupon_validity(self):
        coupon = Coupon.objects.create(
            discount="10.00",
            code="DISCOUNT10",
            valid=True,
            event=self.event
        )

        response = self.client.get(reverse("coupon-validity", args=[coupon.code]))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Coupon is valid")
        self.assertEqual(response.data["discount"], "10.00")

    def test_check_invalid_coupon(self):
        response = self.client.get(reverse("coupon-validity", args=["INVALIDCODE"]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Coupon is not valid")
