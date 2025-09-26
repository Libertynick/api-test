import json

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiOrderCreate(BaseApi):
    """api/order/create"""

    def post_order_create(self, data: json):
        """Запрос POST на api/order/create"""
        post_url = Endpoints.post_order_create
        self.response_data = self.http_methods.post(post_url, body=data).json()

        return self.response_data
