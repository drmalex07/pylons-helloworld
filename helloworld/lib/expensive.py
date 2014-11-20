import logging
import json

from beaker.cache import cache_regions, cache_region

log = logging.getLogger(__name__)

class NameConverter(object):
    def __init__(self):
        pass

    @cache_region('short_term', 'convert_name')
    def convert(self, name):
        log.info("Converting name %s to upper/lower ..." %(name))
        res = {
            'lower': name.decode('utf-8').lower(),
            'upper': name.decode('utf-8').upper()
        }
        return res
