# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

"""
API transform handler. Returns transformed data.
"""

from tornado.gen import coroutine
from koi.base import BaseHandler

from transformation.models import transform
from transformation.helpers.assets_helper import validate_post_request


class AssetsHandler(BaseHandler):
    """
    Responsible for transforming Raw Data about Assets to triples data
    """

    @coroutine
    def post(self):
        """Respond with transformed data"""
        data_format, body = validate_post_request(self.request)

        data = yield transform.transform(
            body, data_format, self.get_argument("r2rml_url", None))

        self.finish({'status': 200, 'data': data})
