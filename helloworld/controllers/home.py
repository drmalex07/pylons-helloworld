import logging
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import app_globals as g

from helloworld.lib.base import BaseController, render

import helloworld.lib.helpers as h


log = logging.getLogger(__name__)

class HomeController(BaseController):

    def index(self):
        log.info('Entered HomeController.index() method')
        return 'Hello World';

    def test302(self):
        ## Note: url() recognizes 'host','protocol' named parameters as having a special meaning
        ## All other non-special parameters are urlencoded and appended as GET query parameters
        #u = url("/greet/greet/koukouroukou", foo="bar", boo="far")
        # or ...
        # Note: url() can also generate a URL given the internal controller/action/id details
        u = url(controller='greet', action='greet', id='koukouroukou', foo='bar', boo='far')
        log.info('Entered HomeController.test302() method: Redirecting to %r' %(u))
        redirect(u);

    def dump(self):
        return 'v = %s ' % (g.version_1)

    def test403(self):
        log.info('Entered HomeController.test4xx() method: Sending an error page')
        abort(403, detail='This is a test on 4xx errors')

    def test404(self):
        log.info('Entered HomeController.test4xx() method: Sending an error page')
        abort(404)
