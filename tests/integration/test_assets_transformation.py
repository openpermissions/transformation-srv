# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


import json
import os
from mock import MagicMock
from tornado.concurrent import Future, DummyExecutor

from koi import define_options
from koi.test_helpers import gen_test

from transformation.app import CONF_DIR

from transformation.controllers.assets_handler import AssetsHandler
from transformation.models.transform import AsyncHTTPClient

AssetsHandler.executor = DummyExecutor()
handler = AssetsHandler(MagicMock(), MagicMock())

INPUT1 = {'source_id_types': 'MaryEvansPictureID',
          'source_ids': '100123',
          'description': 'Sunset over a Caribbean beach'}

# Set to True to send request to real Karma
LIVE_SERVICE = False


def setup_function(function):
    define_options(os.path.join(CONF_DIR, 'default.conf'))
    handler.finish = MagicMock()

    if not LIVE_SERVICE:
        future = Future()

        class C:
            pass

        C.body = json.dumps(INPUT1)
        C.code = 200
        future.set_result(C)

        AsyncHTTPClient.fetch = MagicMock(return_value=future)

    def get_arg(arg, default):
        if default:
            return default
        return None

    handler.request.get_argument = get_arg


@gen_test
def test_csv_post_with_four_assets():
    handler.request.headers = {'Content-Type': 'text/csv; charset=utf-8'}
    handler.request.body = \
        'source_id_types,source_ids,description\n' + \
        'MaryEvansPictureID,100123,Sunset over a Caribbean beach\n' + \
        'MaryEvansPictureID,100456,Polar bear on an ice floe\n' + \
        'MaryEvansPictureID,999001,Johnny Depp as Sweeney Todd\n' + \
        'MaryEvansPictureID,999002,Evening street view Paris 1910'

    yield handler.post()
    assert handler.finish.call_count == 1
    assert handler.get_status() == 200
    if LIVE_SERVICE:
        print handler.finish.call_args


@gen_test
def test_csv_post_with_four_assets_with_missing_optional_data():
    handler.request.headers = {'Content-Type': 'text/csv; charset=utf-8'}
    handler.request.body = \
        'source_id_types,source_ids,description\n' + \
        'MaryEvansPictureID,100123,\n' + \
        'MaryEvansPictureID,100456,Polar bear on an ice floe\n' + \
        'MaryEvansPictureID,999001,Johnny Depp as Sweeney Todd\n' + \
        'MaryEvansPictureID,999002,Evening street view Paris 1910'

    yield handler.post()
    assert handler.finish.call_count == 1
    assert handler.get_status() == 200
    if LIVE_SERVICE:
        print handler.finish.call_args


@gen_test
def test_json_post_with_four_assets_with_missing_optional_data():
    handler.request.headers = {'Content-Type': 'application/json; charset=utf-8'}
    handler.request.body = [
        {
            "source_ids": [
                {
                    "source_id_type": "MaryEvansPictureID",
                    "source_id": "100123456"
                }
            ],
            "offer_ids": [
                "1",
                "2",
                "3",
                "4"
            ],
            "description": "Sunset over a Caribbean beach"
        },
        {
            "source_ids": [
                {
                    "source_id": "100456123",
                    "source_id_type": "MaryEvansPictureID"
                },
                {
                    "source_id_type": "AnOtherPhotoID",
                    "source_id": "999002222"
                }
            ],
            "offer_ids": [
                "1",
                "2",
                "3",
                "4"
            ],
            "description": "Polar bear on an ice floe"
        }
    ]
    handler.request.body = json.dumps(handler.request.body)
    yield handler.post()
    assert handler.finish.call_count == 1
    assert handler.get_status() == 200
    if LIVE_SERVICE:
        print handler.finish.call_args
