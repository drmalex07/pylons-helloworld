"""Setup the helloworld application"""
import logging

import pylons.test

from helloworld.config.environment import load_environment
from helloworld.model import Base, Session, init_model

def setup_app(command, conf, vars):
    """Place any commands to setup helloworld here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    # Setup database
    logging.info("Creating tables")
    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)
    logging.info("Successfull setup")
