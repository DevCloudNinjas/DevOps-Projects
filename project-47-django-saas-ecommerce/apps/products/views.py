from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views import View
from django.views.generic import DetailView, ListView

# Django Rest Framework lib
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
# Stripe lib
import stripe

# Models and serializer
from .serializer import ProductSerializer , ProductEditableSerializer
from .models import PaymentHistory, Price, Product



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
stripe.api_key = 'sk_test_51LXmPhI1Paqp8Qt3Tca8GhuEe1FI2bKbkscog7ORAiGRL00QsAKVgMaSwQ8RXUnM4Y3GwVC2BHLdZwoswI8dY0ax00GBNzBHsK'


# @cache_page(timeout=60 * 30)  # cache for 30 minutes
class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "products/product_list.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context["prices"] = Price.objects.filter(product=self.get_object())
        return context


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(price.price) * 100,
                        "product_data": {
                            "name": price.product.name,
                            "description": price.product.desc,
                            "images": [
                                f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
                            ],
                        },
                    },
                    "quantity": price.product.quantity,
                }
            ],
            metadata={"product_id": price.product.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            product_id = session["metadata"]["product_id"]
            product = get_object_or_404(Product, id=product_id)

            send_mail(
                subject="Here is your product",
                message=f"Thanks for your purchase. The URL is: {product.url}",
                recipient_list=[customer_email],
                from_email="test@gmail.com",
            )

            PaymentHistory.objects.create(
                email=customer_email, product=product, payment_status="completed"
            )

        # Can handle other events here.

        return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = "products/success.html"


class CancelView(TemplateView):
    template_name = "products/cancel.html"
 
 
    
    
# Viewset
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductTransactionViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action in ["update", "partial_update", "create"]:
            return ProductEditableSerializer
        return ProductSerializer     
    
