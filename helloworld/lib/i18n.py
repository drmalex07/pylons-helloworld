from pylons.i18n import _ as _t

class DeferredTranslator(object):
    def __init__(self, s):
        self.s = s
    def __unicode__(self):
        return _t(self.s)

