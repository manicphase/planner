import json

from test import AcceptanceTestCase


class ApiTest(AcceptanceTestCase):
    def test_api_user_can_add_schedule_and_view_an_engagement(self):
        resp = self.client.get('/api/read/Engagement')
        self.assertEquals(200, resp.status_code)
        self.assertEquals(json.loads(resp.data), {"data": []})
