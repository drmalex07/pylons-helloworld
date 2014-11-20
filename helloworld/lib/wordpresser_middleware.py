import requests
import urlparse
import pylons
from pylons.util import call_wsgi_application

import logging
log = logging.getLogger(__name__)

class WordpresserMiddleware(object):

    BLOCK_SIZE=4096

    def __init__(self, app, proxy_host, path_prefix=''):
        #log.info ('Entering middleware ctor ...')
        self.app = app
        self.proxy_host = urlparse.urlparse(proxy_host)
        self.path_prefix = path_prefix.strip()
        return

    def __call__(self, environ, start_response):
        #log.debug ('** environ=\n%s' %(self.object_dumps(environ)))
        status_text, headers, app_iter = call_wsgi_application (self.app, environ, catch_exc_info=False)
        method = environ.get('REQUEST_METHOD')
        path   = environ.get('PATH_INFO')
        qs     = environ.get('QUERY_STRING')
        if status_text.startswith("404") and path.startswith(self.path_prefix):
            # The resource was not found: reverse-proxy this request to wordpress host
            path = path [len(self.path_prefix):]
            req_url = self.proxy_host.scheme + "://" + self.proxy_host.netloc + self.proxy_host.path + path + "?" + qs
            req_headers = self.request_headers(environ)
            log.info ('Proxying to URL: %s' %(req_url))
            # Proxy request
            res = None
            if method == 'GET':
                res = requests.get (req_url, headers=req_headers, stream=True)
            elif method == 'POST':
                with environ.get('wsgi.input') as reader:
                    req_data = reader.read()
                res = requests.post (req_url, headers=req_headers, data=req_data, stream=True)
            # Handle proxied request's result
            if res and res.ok:
                # succeded: return it's response
                log.info ("Proxied request (%s %s) succeded!" %(method, req_url))
                start_response ("%s %s" %(res.raw.status, res.raw.reason),
                    filter(lambda t: not (t[0] in ['server', 'x-pingback', 'x-powered-by']), res.headers.items()))
                return self.response_body_generator(res)
            else:
                # failed: return original Pylons response
                log.warning ("Proxied request (%s %s) failed: returning original 404 response" %(method, req_url))
                start_response (status_text, headers)
                return app_iter
        else:
            # The resource was either found or rejected: nop
            start_response (status_text, headers)
            return app_iter
        pass

    def request_headers(self, environ):
        r = {}
        # Copy all current request headers
        for k in environ.keys():
            if k.startswith('HTTP_'):
                k1 = (k[5:]).lower().replace('_','-')
                r[k1] = environ.get(k)
        # Specify the content-type
        r['content-type'] = environ.get('CONTENT_TYPE')
        # The 'Host' header should be replaced
        r['host'] = self.proxy_host.netloc
        r['x-forwarded-for']  = environ.get('REMOTE_ADDR')
        r['x-forwarded-host'] = environ.get('HTTP_HOST')
        return r

    @classmethod
    def response_body_generator(cls, res):
        while 1:
            s = res.raw.read(cls.BLOCK_SIZE)
            if len(s):
                yield s
            else:
                break

    @classmethod
    def object_dumps(cls, environ):
        import json
        d = {}
        for k in environ.keys():
            d[k] = repr(environ[k])
        return json.dumps(d, indent=4)
