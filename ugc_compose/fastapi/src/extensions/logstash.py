import logging
from typing import Optional

import logstash

logstash_handler: Optional[logstash.handler_udp.LogstashHandler] = None


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = record.args.get('request_id')
        return True
