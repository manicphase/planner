import json

from test import AcceptanceTestCase
from planner.model import Engagement


class ApiTest(AcceptanceTestCase):
    def test_api_user_can_add_schedule_and_view_an_engagement(self):
        self.maxDiff = None
        resp = self.client.get('/api/read/Engagement')
        self.assertEquals(200, resp.status_code)
        self.assertEquals({"data": []}, json.loads(resp.data))

        engagement = Engagement(name="Test", revenue=0, isrnd=False)
        resp = self.client.post('/api/create/Engagement',
                                content_type="application/json",
                                data=json.dumps(engagement.to_dict()))
        self.assertEquals(200, resp.status_code)
        self.assertEquals("OK", resp.data)

        resp = self.client.get('/api/read/Engagement')
        data = json.loads(resp.data)['data']
        self.assertEquals(200, resp.status_code)
        self.assertTrue(len(data) == 1)
        self.assertEquals(engagement, Engagement.from_dict(data[0]))
