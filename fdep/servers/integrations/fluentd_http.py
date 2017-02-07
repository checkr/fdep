"""Integrate Fluentd with fdep.

Pass the ``--fluentd_http_url=http://..`` option or add the ``FLUENTD_HTTP_URL`` environment variable when you run ``fdep serve``.


The source for the integration in your fluentd service should be like this:

.. code:: xml

   <source>
     @type http
     format json
   </source>
"""
import json
import sys

import requests
from fdep.servers.integrations import Integration


class FluentdHttpIntegration(Integration):

    def __init__(self, fluentd_http_url):
        self.fluentd_http_url = fluentd_http_url

    def after_function(self, func_name, args, kwargs, result):
        status_code = requests.post(
            self.fluentd_http_url,
            data=json.dumps({
                "func_name": func_name,
                "args": args,
                "kwargs": kwargs,
                "result": result
            })
        ).status_code
        if status_code >= 400:
            sys.stderr.write("Fluentd transmission failed.\n")
