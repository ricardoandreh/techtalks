from coupon.models import Coupon
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ModelSerializer


class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

    def validate_event(self, value):
        request = self.context.get("request")
        if value.organizer != request.user:
            raise PermissionDenied("You can only create coupons for your own events.")
        return value
