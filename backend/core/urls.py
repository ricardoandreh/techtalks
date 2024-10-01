from coupon.views import CheckCouponValidityView, CouponViewSet
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from event.views import EventViewSet
from organizer.views import OrganizerRegisterView, OrganizerViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

router = DefaultRouter()
router.register(r"organizers", OrganizerViewSet)
router.register(r"events", EventViewSet)
router.register(r"coupons", CouponViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API
    path("api/", include(router.urls)),
    path("api/coupon-validity/<str:code>/", CheckCouponValidityView.as_view(), name="coupon-validity"),
    # Testing Request
    path("helloworld/", lambda _: JsonResponse({"hello": "world"})),
    # Auth (Simple JWT)
    path("api/register/", OrganizerRegisterView.as_view(), name="organizer-register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
