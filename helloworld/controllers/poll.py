import logging
import cgi

from pylons import config
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from helloworld.lib.base import BaseController, render

import helloworld.model as model
import helloworld.lib.helpers as h

import webhelpers.pylonslib.secure_form as secure_form

log = logging.getLogger(__name__)

class PollController(BaseController):

    def results(self):
        log.info ('Viewing poll results')
        db_session = model.Session()
        q1 = db_session.query(model.Vote.vote, model.func.count(model.Vote.vote)).group_by(model.Vote.vote)
        c.vote_freqs = q1.all()
        q2 = db_session.query(model.Vote)
        c.vote_count = q2.count()
        db_session.close()
        return render('poll/results.html')

    def brk(self):
        raise Exception("break")

    def vote(self):
        if request.method == 'POST':
            return self._vote_save()
        log.info ('Generating a form to vote')
        c.csrf_token_field = secure_form.auth_token_hidden_field()
        return render('poll/vote.html')

    def _vote_save(self):
        post = request.POST

        # Fetch POST data
        vote = post.get(u'vote')
        email = post.get(u'email')
        op = post.get(u'op')
        attachment = post.get(u'vote-attachment')
        comment = post.get(u'vote-comment')
        fp = attachment.file if isinstance(attachment, cgi.FieldStorage) else None
        attachment_data = fp.read(256).decode('utf-8') if fp else '<None>' # Note: assume plain text utf-8 file
        #raise Exception('Inspect POST data')

        # Validate request
        if not (post.get(secure_form.token_key, None) == secure_form.authentication_token()):
            abort (403, detail=u'Not permitted (possible CSRF attack)')

        # Validate POST data: in practice we should not abort but rather redirect to the form
        # with all the errors highlighted
        vote = int(vote)
        if not (vote >= 0 and vote <= 10):
            abort (400, detail=u'Bad value for vote')

        # Done with validation, now just log this and store the (vote,email) in the underlying model
        log.info ('Saving vote for poll (%r)' %(dict(vote=vote, email=email, op=op, attachment_data=attachment_data)))
        db_session = model.Session()
        v = model.Vote (vote=vote, email=email, created_at=None, description=comment);
        db_session.add(v)
        db_session.commit()

        # Done with form processing, redirect to a normal (GET) request ...
        h.flash('Your vote is saved!')
        redirect (url(controller='poll', action='results'))
        return
