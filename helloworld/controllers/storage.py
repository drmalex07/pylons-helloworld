import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylons import config
from paste.deploy.converters import asbool

from helloworld.lib.base import BaseController, render

import webhelpers.pylonslib.secure_form as secure_form
import cgi
import os
import re
from datetime import datetime

log = logging.getLogger(__name__)

STORAGE_ROOT_DIR = config.get('storage.root_directory')

class StorageController(BaseController):

    def file(self):
        ''' Fetch a file resource '''
        # Todo: Determine the appropriate content-type, force download
        response.headers['content-type'] = 'text/plain; charset=utf-8'
        return '<contents of <%s>>' %(request.params.get('path'))

    def index(self):
        ''' Display a directory listing '''
        relpath = request.params.get('path', '/')
        relpath = re.sub(r'[\.]+', ".", relpath)
        abspath = os.path.join (STORAGE_ROOT_DIR, relpath.strip(' /'))
        if not os.path.isdir(abspath):
            abort (400, detail=u'The path (%s) does not map to a directory' %(abspath))
        listing = []
        for f in os.listdir(abspath):
            pf = os.path.join (abspath, f)
            is_dir = os.path.isdir(pf)
            is_file = os.path.isfile(pf)
            if (is_dir or is_file):
                sf = os.stat(pf)
                target = None
                if is_dir:
                    target = url(controller='storage', action='index',
                        path = relpath.strip(' /') + '/' + f)
                else:
                    target = url(controller='storage', action='file',
                        path = relpath.strip(' /') + '/' + f)
                entry = dict(
                    is_dir = is_dir,
                    is_file = is_file,
                    name = f,
                    target = target,
                    size = sf.st_size,
                    created = datetime.fromtimestamp(sf.st_ctime),
                    modified = datetime.fromtimestamp(sf.st_mtime))
                listing.append (entry)
        c.storage_index = {
            'listing': listing,
            'path': relpath,
            'upload_url': url(controller='storage', action='upload_handle')
        }
        return render('storage/index.html')
        pass

    def upload_handle(self):
        ''' Handle a file upload and store it properly under a path '''
        post = request.POST

        path = post.get(u'path')
        upload = post.get(u'upload')
        ifp = upload.file if isinstance(upload, cgi.FieldStorage) else None
        # Todo: do somehing with file object ifp at given path 

        log.info ("upload_handle(): POST=%r" %(post.items()))
        redirect (url(controller='storage', action='index'))
        pass
