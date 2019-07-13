import logging
from scrapy.exceptions import IgnoreRequest

class SkipCriteria(object):
    def process_response(self, request, response, spider):
        return response
    def process_exception(request, exception, spider):
        pass
