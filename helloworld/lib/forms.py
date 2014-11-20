import formencode
import re

from formencode import validators

re1 = re.compile('^[a-z]{3,3}[-][\d]{4,4}$') # e.g. "abc-0945"

class ContactForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    # Define form fields 
    email = validators.Email(not_empty=True, strip=True)
    comments = validators.String(not_empty=True, strip=True)
    order_code = validators.Regex(not_empty=True, strip=True, regex=re1)

    # Define "post-process" or "pre-process" validators
    chained_validators = []
    pre_validators = []


class DummyValidator(formencode.FancyValidator):
    ''' Define a custom validator by overriding base methods '''

    def _convert_to_python(self, value, state):
        return str(value)

    def _validate_python(self, value, state):
        ''' raise Invalid if the input is invalid, otherwise return anything '''
        return


