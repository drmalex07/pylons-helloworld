'''
Add custom commands to paster
'''

import os, os.path, logging

from paste.script.command import Command
from paste.registry import Registry
from paste.script.util.logging_config import fileConfig

class HelloworldCommand(Command):
    '''
    A base class to use when the full Pylons environment should be loaded
    '''
    summary = __doc__.split("\n") [0]
    usage = __doc__
    group_name = "helloworld"
    
    def __init__(self, name):
        Command.__init__(self, name)
        self.parser = Command.standard_parser(verbose=False)
        self.parser.add_option('-c', '--config', dest='config', default='development.ini', help='Config file to use.')
        return

    def command(self):
        pass
    
    def _load_config(self):
        from paste.deploy import appconfig
        if not self.options.config:
            msg = 'No config file supplied'
            raise self.BadCommand(msg)
        self.filename = os.path.abspath(self.options.config)
        if not os.path.exists(self.filename):
            raise AssertionError('Config filename %r does not exist.' % self.filename)
        fileConfig (self.filename)
        conf = appconfig('config:' + self.filename)
        # We have now loaded the config. Now we can import helloworld for the first time.
        from helloworld.config.environment import load_environment
        load_environment (conf.global_conf, conf.local_conf)

        self.registry = Registry()
        self.registry.prepare()
        return

class Echo(Command):
    '''
    Just echo the supplied arguments (no environment is loaded)

    e.g. paster hello-echo --foo bar --file /tmp/hello.txt a1 a2 a3

    '''
    summary = __doc__.split("\n") [0]
    usage = __doc__
    group_name = "helloworld"
    
    def __init__(self, name):
        # Init base class
        Command.__init__(self, name)
        # Parser configuration
        self.parser.add_option("-f", "--file", dest="file", help="write report to FILE", metavar="FILE")
        self.parser.add_option("-x", "--foo", dest="foo", help="assign a value for foo", metavar="FOO")
        self.parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
        return
    
    def command(self):
        print "Hello (paster) world!"
        print
        print "My options are: -\n  %r" %(self.options)
        print "My args are: -\n  %r" %(self.args)
        print
        print "My parser help is:"
        print self.parser.format_help()
        return

class Hello(HelloworldCommand):
    '''
    Just echo the supplied arguments (with full environment loaded!)

    e.g. paster hello-hello --config test.ini --foo bar --file /tmp/hello.txt a1 a2 a3

    '''
    summary = __doc__.split("\n") [0]
    usage = __doc__
    group_name = "helloworld"

    def __init__(self, name):
        # Init base class
        HelloworldCommand.__init__(self, name)
        # Parser configuration (self.parser is allready created from base class)
        self.parser.add_option("-f", "--file", dest="file", help="write report to FILE", metavar="FILE")
        self.parser.add_option("-x", "--foo", dest="foo", help="assign a value for foo", metavar="FOO")
        self.parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
        return

    def command(self):
        # Load the app environment
        self._load_config()
        # Echo your input args ...
        print "Hello (paster+helloworld) world!"
        print
        print "My options are: -\n  %r" %(self.options)
        print "My args are: -\n  %r" %(self.args)
        # Test your environment (registry) ...
        print "Registry: -\n  %r" %(self.registry)
        # Test your environment (model) ...
        import helloworld.model as model
        db_session = model.Session();
        print "Model: -\n  The 'votes' table has %d records" %(db_session.query(model.Vote).count())
        db_session.close()
        return

class InitDb(HelloworldCommand):
    group_name = "helloworld"

    def __init__(self, name):
        # Init base class
        super(InitDb,self).__init__(name)
        return

    def command(self):
        # Load the app environment
        self._load_config()
        # Create database tables 
        import helloworld.model as model
        db_session = model.Session();
        logging.info("Creating tables at %s" %(db_session.bind))
        model.Base.metadata.create_all (bind=db_session.bind)
        db_session.close()
        return

