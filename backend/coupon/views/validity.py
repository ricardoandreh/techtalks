from coupon.models import Coupon
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CheckCouponValidityView(APIView):
    def get(self, request, code):
        try:
            coupon = Coupon.objects.get(code=code, valid=True)
            return Response({
                "message": "Coupon is valid",
                "discount": str(coupon.discount)
            }, status=status.HTTP_200_OK)
        except Coupon.DoesNotExist:
            return Response({
                "message": "Coupon is not valid"
            }, status=status.HTTP_404_NOT_FOUND)
