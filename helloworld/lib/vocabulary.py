# -*- encoding: utf-8 -*-

import re, time, datetime

#from helloworld.lib.i18n import DeferredTranslator as _
from pylons.i18n import lazy_ugettext as _

vocabulary = {
    'thematic_category': [
        ('health', _('Health')),
        ('environment', _('Environment')),
        ('education', _('Education')),
        ('economy', _('Economy')),
        ('society', _('Society')),
        ('defense', _('Defense')),
        ('location', _('Location')),
        ('transports', _('Transports')),
        ('administration', _('Administration')),
        ('government', _('Government')),
        ('geography', _('Geography')),
        ('public-spending', _('Public Spending')),
        ('politics', _('Politics')),
    ],
}


