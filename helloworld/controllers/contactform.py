import logging
import formencode

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import webhelpers.pylonslib.secure_form as secure_form

from helloworld.lib.base import BaseController, render

from helloworld.lib.forms import ContactForm

log1 = logging.getLogger(__name__)

class ContactformController(BaseController):
    ''' An demo for using formencode for creating/validating forms
    '''

    def __after__(self):
        session.save()

    def contact(self):
        if request.method == 'POST':
            redirect_url = self._process_contact()
            redirect(redirect_url)
        log1.info ('Generating a form ...')
        c.csrf_token_field = secure_form.auth_token_hidden_field()
        c.errors = session.get('contactform.errors', None)
        c.values = session.get('contactform.values', {})
        return render('contactform/contact.html')

    def _process_contact(self):

        # Validate secure_form's (CSRF protection) token

        if not (request.params.get(secure_form.token_key) == secure_form.authentication_token()):
            abort (403, detail=u'Not permitted (possible CSRF attack)')

        # If cancelled, dont do anything

        if request.params.get('op') != 'Submit':
            session.pop('contactform.errors', None)
            session.pop('contactform.values', None)
            return url(controller='contactform', action='nevermind')

        # Validate form fields ...

        schema = ContactForm()
        try:
            fields = schema.to_python(dict(request.params))
            session.pop('contactform.errors', None)
            session.pop('contactform.values', None)
            self._save_contact(fields, schema)
            return url(controller='contactform', action='thanks')
        except formencode.Invalid, ex:
            session.update({
                'contactform.errors': ex.error_dict,
                'contactform.values': ex.value,
            })
            return url(controller='contactform', action='contact')

        return None

    def _save_contact(self, fields, field_schema):
        # Persist (or anything usefull) with the validated and converted 
        # form data.
        #raise Exception ('Inspect')
        log1.info ('Saving contact form-data: %s' %(repr(fields)))
        pass

    def thanks(self):
        return '<p>Thank you for contacting us!</p>'

    def nevermind(self):
        return '<p>Nevermind, come back later!</p>'

