
from helloworld.tests import *

class TestPollController(TestController):

    @classmethod
    def setup_class(cls):
        pass
  
    @classmethod
    def teardown_class(cls):
        pass

    def test_results(self):
        res1 = self.app.get(url(controller='poll', action='results'))

    def test_vote(self):
        res1 = self.app.get(url(controller='poll', action='vote'))
