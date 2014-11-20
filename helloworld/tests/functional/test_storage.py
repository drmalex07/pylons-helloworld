from helloworld.tests import *

class TestStorageController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='storage', action='index'))
        # Test response...
