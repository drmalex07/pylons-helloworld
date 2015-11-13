import pylons
from pylons.util import ContextObj, PylonsContext

from helloworld.tests import *
from helloworld.lib.base import render

class TestGreetController(TestController):

    ## Helpers ##

    @classmethod
    def _setup_template_context(cls):
        '''Setup Pylons global tmpl_context (c)
        '''
        c1 = ContextObj()
        pylons_context = PylonsContext()
        pylons_context.tmpl_context = c1 
        pylons.tmpl_context._push_object(c1)

    @classmethod
    def _teardown_template_context(cls): 
        '''Teardown Pylons global tmpl_context (c)
        '''
        pylons.tmpl_context._pop_object()

    @classmethod
    def _setup_request_globals(cls, response):
        ''' Setup Pylons globals (request, response, session) 
        for an emulated request. 
        
        Args:
            response is the response from an instance of webtest.TestApp 
        
        '''
        pylons.request._push_object(response.req)
        pylons.response._push_object(response.response)
        pylons.session._push_object(None)
    
    @classmethod
    def _teardown_request_globals(cls):
        '''Teardown Pylons globals (request, response, session)
        '''
        pylons.request._pop_object()
        pylons.response._pop_object()
        pylons.session._pop_object()

    ## Tests ##

    def test_render(self):
        ''' An example of using Pylons globals after the test request
        has been completed.
        '''
        
        response = self.app.get(url(controller='greet', action='index'))
        
        self._setup_template_context()
        self._setup_request_globals(response)
       
        from pylons import tmpl_context as c
        c.author = 'Foo'
        c.maintainer = 'Boo'
        
        markup = render('greet/index-1.html', extra_vars={ 'foo': 'bar' })

        self._teardown_request_globals()
        self._teardown_template_context()
         
    def test_greet(self):
        ''' A typical test on the response of an actual controller 
        '''
        response = self.app.get(url(controller='greet', action='greet', id='lalakis'))
        assert response.pyquery('h3')


