from helloworld.tests import *

class TestContactformController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='contactform', action='index'))
        # Test response...
