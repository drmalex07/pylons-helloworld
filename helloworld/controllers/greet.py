# -*- encoding: utf-8 -*-

import logging
import json

from pylons import request, response, config, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylons.i18n import get_lang, set_lang, _

from helloworld.lib.base import BaseController, render

from helloworld.lib.expensive import NameConverter

log = logging.getLogger(__name__)

class GreetController(BaseController):

    ## Define the __after__, __before__ wrapper methods 

    def __before__(self):
        log.info ('Preparing controller to handle response');
        # Prepare session-based data
        self._update_counter()
        self._setup_language()
        return

    def __after__(self):
        log.info ('Closing controller after handling response');
        session.save()
        return

    ## Define helper methods ##

    def _update_counter(self):
        ''' Update session-based counters '''
        # Note: Any pickleable object can be stored into session storage
        if not session.has_key('count'):
            session['count'] = 0;
        if ('clear' in request.params.keys()) and (not (request.params['clear'] == 'no')):
            session['count'] = 0;
        else:
            session['count'] += 1;
        return

    def _setup_language(self):
        ''' Setup response language based on specific request parameter or session preference '''

        if not (session.has_key('prefs')):
            session['prefs'] = {};

        lang = None
        if (request.params.has_key('lang')):
            lang = request.params['lang']
            session['prefs']['lang'] = lang
        else:
            lang = session['prefs'].get('lang', None)
        log.info ('Using language "%s"' %(lang))
        set_lang(lang)

    ## Methods exposed as controller actions ##

    def index(self, id = None):
        log.info ('Entering index() controller');
        # Note: You can add custom response headers ...
        response.headers['x-author-name'] = u'lalakis'
        # Note: You can pass variables to the templating engine via
        #  - c : attach properties to the request-local tmpl_context object 
        #  - extra_vars 
        c.author = u'malex'
        c.maintainer = u'λαλάκης'
        return render ("greet/index.html", extra_vars = {'foo': 'bar'});

    def greet(self, id = "nobody"):
        s = u'''<html><body><h3>{greeting:s}</h3><p>This is your <code>{count_visits:d}</code>th visit</p></body></html>'''
        return s.format(greeting = _('Hello %(name)s') %(dict(name=id)), count_visits = session['count']);

    def brk(self):
        raise Exception('Break')

    def category_list(self):
        ''' An example of howto load a static dict of translatable strings. 
        (using our DeferredTranslator or lazy_ugettext)
        '''
        from helloworld.lib.basic_vocabulary import vocabularies
        
        c.categories = vocabularies.get('thematic_category', [])
        c.title = _('Thematic Category')

        return render("greet/categories.html")

    def debug_translated_messages(self):
        from helloworld.lib.inspire_vocabulary import vocabularies
        
        # These terms are marked as translatable by our custom Babel
        # extractor (that's why we can pass them to ugettext)
        c.categories = [ (term[0], _(term[1])) \
            for term in vocabularies.get('party_roles', []) ]
        c.title = _('Party Roles')
                
        return render("greet/categories.html")

    def dump(self,id=''):
        response.headers['content-type'] = "application/json; charset=utf-8";
        return json.dumps(dict(request.params), indent=4) +"\r\n"

    def convert_name(self, name):
        ''' This action will call an expensive method managed by beaker's cache_regions '''
        response.headers['content-type'] = "application/json; charset=utf-8";
        res = NameConverter().convert(name)
        return json.dumps(res, indent=4)



