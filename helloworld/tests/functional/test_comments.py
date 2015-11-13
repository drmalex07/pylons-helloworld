from helloworld.tests import *

class TestCommentsController(TestController):

    def test_index(self):
        response = self.app.get(url('comments'))
        # Test response...

    def test_create(self):
        response = self.app.post(url('comment-create'))

    def test_new(self):
        response = self.app.get(url('comment-new'))

    def test_update(self):
        response = self.app.put(url('comment-update', cid=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('comment-update', cid=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('comment-delete', cid=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('comment-delete', cid=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('comment-show', cid=1))

    def test_edit(self):
        response = self.app.get(url('comment-edit', cid=1))
