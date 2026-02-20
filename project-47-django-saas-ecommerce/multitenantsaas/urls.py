# Django Settings
from django.contrib import admin
from django.views import generic
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings

# Graphql
# graphQL
from apps.finances.schema import schema
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# Django Rest Framework
from rest_framework import routers, permissions , views, serializers, status
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


# Utils and Libraries
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# Apps
from apps.snippets import urls as snippets_urls
from apps.finances import urls as finances_urls
from apps.payments import urls as payment_urls
from apps.home import urls as home_urls
from apps.products import urls as product_urls
# ViewSet
from apps.snippets.views import SnippetsViewSet
from apps.finances.views import AccountViewSet , TransactionViewSet, CategoryViewSet
from apps.products.views import ProductViewSet , CreateStripeCheckoutSessionView


router = routers.DefaultRouter()
router.register(r'router/snippets', SnippetsViewSet, basename="snippets")
router.register(r'router/accounts', AccountViewSet, basename="accounts")
router.register(r'router/transactions', TransactionViewSet, basename="transactions")
router.register(r'router/categories', CategoryViewSet, basename="categories")
router.register(r'router/products', ProductViewSet, basename="products")

urlpatterns = router.urls

user_list = SnippetsViewSet.as_view({'get': 'list'})
user_detail = SnippetsViewSet.as_view({'get': 'retrieve'})

schema_view = get_schema_view(
    openapi.Info(
        title="Multi-tenant SaaS Application",
        default_version='v1',
        description="Microservices built by Joel Otepa Wembo",
        terms_of_service="https://domain.io/policies/terms/",
        contact=openapi.Contact(email="mail@djangoapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("",  include(router.urls)),
    path('home', include(home_urls)),
    path('api/v1/snippets/', include(snippets_urls)),
    path('api/v1/finances/', include(finances_urls)),
    path('api/v1/payments/', include(payment_urls)),
     path('api/v1/products/', include(product_urls)),
      path(
        "create-checkout-session/<int:pk>/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("__debug__/", include("debug_toolbar.urls")),
    path("data-browser/", include("data_browser.urls")),
    # path('ledger/', include('django_ledger.urls', namespace='django_ledger')),
 
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),   
    
]

# Media Assets
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
