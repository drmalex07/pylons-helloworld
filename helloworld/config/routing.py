"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    m = Mapper (directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    m.minimization = False
    m.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    m.connect('/error/{action}', controller='error')
    m.connect('/error/{action}/{id}', controller='error')
    
    # Add routes only for testing purposes
    if config['global_conf'].get('test'):
        m.connect('test-action', '/tests/{action}', controller='tests') 
        m.connect('test-action-with-id', '/tests/{action}/{id}', controller='tests') 

    with m.submapper(path_prefix='/helloworld') as m1:
        # Add non-default routes
        m1.connect('greet-list-categories', '/greet/categories', controller='greet', action='category_list')
        m1.connect('greet-interactive-break', '/greet/break', controller='greet', action='brk')
        m1.connect('greet-convert-name', '/greet/convert-name/{name}', controller='greet', action='convert_name')
        m1.connect('comments', '/comments/index', controller='comments', action='index')
        m1.connect('comment-new', '/comments/new', controller='comments', action='new',
            conditions=dict(method=['GET']))
        m1.connect('comment-create', '/comments/create', controller='comments', action='create', 
            conditions=dict(method=['POST']))
        m1.connect('comment-update', '/comments/{cid}/update', controller='comments', action='update',
            conditions=dict(method=['PUT', 'POST']))
        m1.connect('comment-delete', '/comments/{cid}/delete', controller='comments', action='delete',
            conditions=dict(method=['DELETE', 'POST']))
        m1.connect('comment-edit', '/comments/{cid}/edit', controller='comments', action='edit',
            conditions=dict(method=['GET']))
        m1.connect('comment-show', '/comments/{cid}', controller='comments', action='show',
            conditions=dict(method=['GET']))
        
        # Add default routes
        m1.connect('/{controller}/{action}')
        m1.connect('/{controller}/{action}/{id}')

    return m
