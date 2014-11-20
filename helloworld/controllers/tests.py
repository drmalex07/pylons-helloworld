# -*- encoding: utf-8 -*-

import logging
import json

from pylons import request, response, config, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from helloworld.lib.base import BaseController, render

log = logging.getLogger(__name__)

class TestsController(BaseController):

    def greet(self, id=None):
        c.author = u'φουφουτος'
        c.maintainer = u'λαλάκης'
        markup = render('greet/index-1.html', extra_vars={ 'foo': 'Bazz'})
        return markup
