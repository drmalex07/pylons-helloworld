"""Pylons environment configuration"""
import os
import sqlalchemy
import logging

from genshi.template import TemplateLoader
from pylons.configuration import PylonsConfig

import helloworld.lib.app_globals as app_globals
import helloworld.lib.helpers
import helloworld.model as model
from helloworld.config.routing import make_map

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()

    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='helloworld', paths=paths)

    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = helloworld.lib.helpers

    # Setup cache object as early as possible
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)

    # Create the Genshi TemplateLoader
    config['pylons.app_globals'].genshi_loader = TemplateLoader(
        paths['templates'], auto_reload=True)

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)

    # Setup the database connection (bind to an engine)

    db_engine = sqlalchemy.create_engine (config['sqlalchemy.url']);
    model.init_model (db_engine)

    return config
