from coupon.models import Coupon
from coupon.permissions import IsOrganizerOfEvent
from coupon.serializers import CouponSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (IsAuthenticated, IsOrganizerOfEvent,)

    def get_queryset(self):
        return Coupon.objects.filter(event__organizer=self.request.user)
