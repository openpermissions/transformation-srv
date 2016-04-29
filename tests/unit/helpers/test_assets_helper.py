# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


import os
import pytest

from koi.exceptions import HTTPError
from tornado.options import options
from koi import define_options
from mock import MagicMock, patch
from transformation.app import CONF_DIR
from transformation.helpers.assets_helper import verify_body_size, \
    check_content_type, validate_post_request


def setup_function(function):
    define_options(os.path.join(CONF_DIR, 'default.conf'))


def test_verify_body_size_too_large():
    errors = []
    request = MagicMock()
    request.headers = {'Content-Length': options.max_post_body_size + 1}
    request.body = " " * (options.max_post_body_size + 1)

    # MUT
    verify_body_size(request, errors)

    assert len(errors) == 1


def test_verify_body_size_okay():
    errors = []
    request = MagicMock()
    request.headers = {'Content-Length': options.max_post_body_size}
    request.body = " " * (options.max_post_body_size)

    # MUT
    verify_body_size(request, errors)

    assert len(errors) == 0


def test_check_content_type_empty():
    errors = []
    request = MagicMock()
    request.headers.get.return_value = ''

    # MUT
    check_content_type(request, errors)

    assert len(errors) == 1


def test_check_content_type_invalid():
    errors = []
    request = MagicMock()
    request.headers.get.return_value = "wibble-wobble"

    # MUT
    check_content_type(request, errors)

    assert len(errors) == 1


def test_check_content_type_valid():
    errors = []
    request = MagicMock()
    request.headers.get.return_value = 'application/json'

    # MUT
    check_content_type(request, errors)

    assert len(errors) == 0


@patch('transformation.helpers.assets_helper.verify_body_size', autospec=True)
@patch('transformation.helpers.assets_helper.check_content_type', autospec=True)
def test_validate_post_no_errors(*args):
    request = MagicMock()
    # MUT
    validate_post_request(request)


@patch('transformation.helpers.assets_helper.verify_body_size', autospec=True)
@patch('transformation.helpers.assets_helper.check_content_type', autospec=True)
def test_validate_post_errors(check_content_type, *args):
    request = MagicMock()

    check_content_type.side_effect = lambda request, errors: errors.append({})

    with pytest.raises(HTTPError):
        validate_post_request(request)
