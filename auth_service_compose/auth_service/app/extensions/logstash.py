import logging
from typing import Optional

import logstash
from flask import request

logstash_handler: Optional[logstash.handler_udp.LogstashHandler] = None


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True
