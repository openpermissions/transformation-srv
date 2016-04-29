# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import logging

from koi.exceptions import HTTPError

from tornado.options import options
from transformation.models import transform


def verify_body_size(request, errors):
    """
    Determines that the size of the body is within the limit of the system.

    :param request: http request
    :param errors: an array of errors which this function appends
    """
    content_length = long(request.headers.get('Content-Length', 0))
    logging.debug("Request size:{}".format(content_length))

    if content_length > int(options.max_post_body_size):
        msg = 'Content length:{} is too large. Max allowed is:{} kbytes'.format(
            content_length, options.max_post_body_size / 1024.0)
        errors.append({'message': msg})


def check_content_type(request, errors):
    """
    Validates if the content type of the request is supported.

    :param request: HTTP request object
    :param errors: an array of errors which this function appends
    """
    content_type = request.headers.get('Content-Type', '')
    if not content_type:
        errors.append({'message': 'Missing Content-Type in header'})
    else:
        data_format = transform.get_data_format(content_type)

        if not data_format:
            msg = 'Unsupported content type: {}'.format(content_type)
            errors.append({'message': msg})

        return data_format


def validate_post_request(request):
    """
    Validates the request for the AssetsHandler post and returns the
    normalised data format (short content type) and body
    Throws a HTTPError if invalid
    :param handler: AssetsHandler
    """
    request = request
    errors = []

    verify_body_size(request, errors)
    data_format = check_content_type(request, errors)

    if len(errors):
        raise HTTPError(400, {'errors': errors})

    return data_format, request.body
