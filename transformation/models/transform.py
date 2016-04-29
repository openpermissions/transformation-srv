# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import urllib
import logging
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine, Return
from tornado.options import options

SCHEMA_TYPE_CSV = 'CSV'
SCHEMA_TYPE_JSON = 'JSON'


def karma_address(output_format):
    """
    Retrieve the address of the Karma service.

    :param output_format: The output format required
    :return: the full URL for the Karma service
    """
    karma_endpoints = {
        'rdf': options.karma_rdf_endpoint,
        'json': options.karma_json_endpoint
    }
    return '{}:{}{}'.format(
        options.url_karma,
        str(options.karma_port),
        karma_endpoints[output_format])


def get_data_format(content_type):
    """
    Function that parses a HTTP type information header and returns a
    content_type for karma if one is available for the content_type
    indicated in the header.

    :param content_type: HTTP content_type header with eventual
                         MIME type included.
    :returns:  karma content type
    """
    if content_type.startswith('text/csv'):
        return SCHEMA_TYPE_CSV
    elif content_type.startswith('application/json'):
        return SCHEMA_TYPE_JSON
    else:
        return None


@coroutine
def transform(input_data, data_format, r2rml_url, karma_timeout=120):
    """
    Transform input data using the schema to our internal representation

    :param schema: string - key for schema to use
    :param input_data: string - raw input data
    :param data_format: string - the type of the input data (csv or json)
    :param r2rml_url: url to karma model mappings
    :return: object containing transformed data and id mapping
    """
    if not r2rml_url:
        if data_format == SCHEMA_TYPE_JSON:
            r2rml_url = options.default_r2rml_mappings_json.format(
                branch=options.karma_repo_branch)
        else:
            r2rml_url = options.default_r2rml_mappings_csv.format(
                branch=options.karma_repo_branch)

    logging.info('transforming a %.2f kb %s file',
                 len(input_data) / 1024.0, data_format)

    result = yield karma_request(
        r2rml_url, input_data, data_format, karma_timeout)

    if result['errors']:
        raise Exception(result['errors'])

    raise Return({'rdf_n3': result['data']})


@coroutine
def karma_request(r2rml_url, input_data, content_type, timeout):
    """
    Performs a HTTP request against Karma REST API
    :param r2rml_url:
    :param input_data:
    :param content_type:
    :param timeout:
    :return: an object of form {'errors':str,'data':str} their
        will either be an error or some data
    """
    http_client = AsyncHTTPClient()
    karma_endpoint = karma_address('rdf')

    try:
        response = yield http_client.fetch(
            karma_endpoint,
            method='POST',
            headers=None,
            request_timeout=timeout,
            body=urllib.urlencode(
                {
                    'RawData': input_data,
                    'ContentType': content_type,
                    'R2rmlURI': r2rml_url
                }
            ))

        response_data = response.body

    except Exception as e:
        logging.exception(e)
        raise Return({'errors': str(e) + ' @' + karma_endpoint, 'data': None})

    raise Return({'errors': None, 'data': response_data})
