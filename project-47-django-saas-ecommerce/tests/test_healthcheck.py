from django.test import SimpleTestCase
from django.urls import reverse


class HealthcheckTests(SimpleTestCase):
    def test_healthz_returns_ok_payload(self):
        response = self.client.get(reverse("healthz"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(response.json(), {"status": "ok"})
