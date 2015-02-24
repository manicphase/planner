from test import AcceptanceTestCase
from bs4 import BeautifulSoup
import datetime
import time
import json


class ParsePage():
    def __init__(self, client):
        self.client = client
        self.resp = self.client.get('/')
        self.data = BeautifulSoup(self.resp.data)

        # this bit is for manual debugging. yes i know i'm going to hell
        print "\n==================================\n"
        print self.data
        print "\n==================================\n"

    def get_timestamp(self, time_tuple):
        dt = datetime.date(*time_tuple)
        timestamp = time.mktime(dt.timetuple())
        return timestamp

    def get_json_set(self, url, request_data={}, request_type="post"):
        request_type = request_type.lower()
        if request_type == "post":
            return_data = self.client.post(url, request_data)
        elif request_type == "put":
            return_data = self.client.put(url, request_data)
        elif request_type == "head":
            return_data = self.client.head(url, request_data)
        elif request_type == "delete":
            return_data = self.client.delete(url, request_data)
        elif request_type == "options":
            return_data = self.client.options(url, request_data)
        elif request_type == "trace":
            return_data = self.client.trace(url, request_data)
        elif request_type == "patch":
            return_data = self.client.patch(url, request_data)
        else:
            return_data = self.client.get(url, request_data)
        return json.loads(return_data)

    # def _get_json_set(self, url, request_data={}, request_type="post"):
    #    return {"costs": [500, 500, 500, 500],
    #            "revenues": [0, 100, 200, 300]}

    def get_finances(self):
        # TODO: change url when API structur is agreed
        data_dict = {"start": self.get_timestamp((2015, 1, 5)),
                     "end": self.get_timestamp((2015, 12, 31)),
                     "set": "finaces",
                     "team": 1}
        url = "/api/data"
        return self.get_json_set(url, request_data=data_dict)

    def revenues(self):
        # TODO: this, properly
        revenues = self.get_finances()["revenues"]
        return revenues

    def costs(self):
        # TODO: this, also
        costs = self.get_finances()["costs"]
        return costs

    def get_revenue_graph(self):
        revenue_graph = self.data.find(id="finance")
        return revenue_graph


class RevenueGraphAcceptanceTest(AcceptanceTestCase):
    def setUp(self):
        super(RevenueGraphAcceptanceTest, self).setUp()
        self.page = ParsePage(self.client)

    def test_revenue_graph(self):
        # Given the team costs 500 in iteration one
        iteration_one_costs = self.page.costs()[0]

        # And the revenue for projects in iteration one is 0
        iteration_one_revenue = self.page.revenues()[0]

        # When I look at the revenue graph on the index page
        self.revenue_graph = self.page.get_revenue_graph()
        self.assertNotEqual(None, self.revenue_graph)

        # Then the graph shows a loss of 500 in iteration one
        gross_earnings = iteration_one_revenue - iteration_one_costs
        self.assertEquals(-500, gross_earnings)
