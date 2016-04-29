# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import os

from koi import define_options

from transformation.app import CONF_DIR
from transformation.models import transform


def setup_module():
    define_options(os.path.join(CONF_DIR, 'default.conf'))


def test_karma_address_rdf():
    address = transform.karma_address('rdf')
    assert address.endswith('/rdf/r2rml/rdf')


def test_karma_address_json():
    address = transform.karma_address('json')
    assert address.endswith('/rdf/r2rml/json')


def test_get_type_csv():
    for t in ['text/csv', 'text/csv; blah blah']:
        content_type = transform.get_data_format(t)
        assert content_type == transform.SCHEMA_TYPE_CSV


def test_get_type_json():
    for t in ['application/json', 'application/json; blah blah']:
        content_type = transform.get_data_format(t)
        assert content_type == transform.SCHEMA_TYPE_JSON


def test_get_type_none():
    for t in ['', '-', '-text/csv']:
        content_type = transform.get_data_format(t)
        assert content_type is None
