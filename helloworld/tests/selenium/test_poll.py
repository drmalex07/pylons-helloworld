'''
An example of a Selenium-based test controller.

This test controller drives a Selenium webdriver and emulates user interaction.

For proper testing, you should be running a docker selenium/* container in order
to send commands to. E.g.:
  
  Start a container and DNAT to port 4444 
  >>> docker create -it -p 4444:4444 --name selenium-firefox-1 --hostname selenium-firefox-1 selenium/standalone-firefox
  
  Export SELENIUM_HOST to environment, so we know not to use a local webdriver
  >>> export SELENIUM_HOST=127.0.0.1 

'''

import os
import logging
import nose.tools
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions # available since 2.26.0

from pylons import config
import helloworld.tests
from helloworld.tests import url, TestController as BaseTestController

class TestController(BaseTestController):
    
    # Todo: Move {setup/teardown}_class into a base class at __init__.py

    @classmethod
    def setup_class(cls):
        cls.site_url = config.get('site_url', 'http://localhost:5000')
        
        selenium_host = os.environ.get('SELENIUM_HOST')
        selenium_port = int(os.environ.get('SELENIUM_PORT', 4444))
        if not selenium_host:
            cls.webdriver = webdriver.Firefox()
        else:
            cls.webdriver = webdriver.Remote(
                command_executor = 'http://%s:%d/wd/hub' % (selenium_host, selenium_port),
                desired_capabilities = {
                    'browserName': 'firefox',
                    'javascriptEnabled': True,
                })
        logging.info('Using Selenium webdriver: %r' % (cls.webdriver))

    @classmethod
    def teardown_class(cls):
        cls.webdriver.quit()

    def __init__(self, *args, **kwargs):
        super(TestController, self).__init__(*args, **kwargs)
        self.app = None # Not running webtest-based tests here

    # Tests

    @nose.tools.istest
    def test_vote(self):
        wd = self.webdriver
        
        form_url = self.site_url + url(controller='poll', action='vote')
        results_url = self.site_url + url(controller='poll', action='results')
        
        redirected_to_results = lambda wd: wd.current_url == results_url
        
        wd.get(form_url)
        
        form_id = wd.find_element_by_tag_name('form').get_attribute('id')

        # Fill form

        inp = wd.find_element_by_name('vote')
        inp.clear()
        inp.send_keys('4')

        inp = wd.find_element_by_name('email')
        inp.clear()
        inp.send_keys('lalakis@example.com')
        
        inp = wd.find_element_by_id('submit-btn')
        inp.click()
        
        # Wait for page to load

        logging.info('Waiting to submit form #%s...' % (form_id))
        WebDriverWait(self.webdriver, 10).until(redirected_to_results)
        logging.info('Form #%s is submitted. Now, check results ...' % (form_id))
        
        # Check results

        assert redirected_to_results(wd)
        msg1 = wd.find_element_by_css_selector('.messages > li')
        assert msg1 and msg1.text.find('Your vote is saved') >= 0
        
        # Save a screenshot for later inspection
        # Note: This can also be done via http://127.0.0.1:4444/wd/hub
        
        screenshot_file = '/tmp/selenium-webdriver.%s-%s.png' % (
            self.__class__.__name__, 'test_vote')
        saved = wd.save_screenshot(screenshot_file)
        assert saved
        logging.info('Saved final screenshot at %s' % (screenshot_file))

    @nose.tools.istest
    def test_results(self):
        # Todo more tests ...
        pass
      
