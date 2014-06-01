# -*- coding: utf-8 -*-
"""Main Controller"""

import os
from datetime import datetime, timedelta

from tg import expose, flash, require, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates
from errorcats.error import ErrorController

from remysmoke.lib.base import BaseController
from remysmoke.model import DBSession, User, Cigarette, Unsmoke
from remysmoke.widgets.graphs import punch_chart, time_chart
from remysmoke.widgets.stats import smoke_stats

__all__ = ['RootController']

api_location = 'facebook.api'
if os.environ.get('OPENSHIFT_APP_NAME'):
    api_location = os.environ.get('OPENSHIFT_DATA_DIR') + api_location
with open(api_location) as api_file:
    facebook_api = api_file.read().strip()


class RootController(BaseController):
    """
    The root controller for the remysmoke application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    error = ErrorController()

    @expose('remysmoke.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict()

    def pick_a_user(self, user_name=None):
        public_users = DBSession.query(User).filter_by(public=True)
        all_public = public_users.all()

        # The currently logged in user should be selectable regardless of
        # publicity.
        if request.identity:
            authenticated_user = request.identity['user']
            if authenticated_user not in all_public:
                all_public.append(authenticated_user)

        # Try to use a provided user name.
        try:
            user = public_users.filter_by(display_name=user_name).one()
        except Exception:
            if request.identity:
                user = authenticated_user
            else:
                user = public_users.first()
        return all_public, user

    @expose('remysmoke.templates.widget')
    def graph(self, user_name=None, **kwargs):
        # Pick one user to look at
        public, user = self.pick_a_user(user_name)
        return_data = {'public_users': public, 'user': user}

        if not user:
            return_data['widget'] = 'No user selected.'
        elif kwargs.get('punchcard'):
            return_data['widget']=punch_chart(user)
        elif kwargs.get('weeks'):
            try:
                weeks=int(kwargs['weeks'])
            except ValueError:
                return self.graph(weeks=1)
            # timeseries graph
            if weeks > 4:
                return_data.update(dict(widget=time_chart(user, weeks, 7), weeks=weeks))
            else:
                return_data.update(dict(widget=time_chart(user, weeks * 7), weeks=weeks))
        else:
            return_data['widget']="Please select a graph type above."
        return return_data

    @expose('remysmoke.templates.stats')
    def stats(self, user_name=None):
        """Show some stats about cigarette consumption."""

        # Pick one user to look at
        public, user = self.pick_a_user(user_name)
        return_data = dict(public_users=public)
        if not user:
            return_data['data']=None
        else:
            return_data.update(dict(user=user, data=smoke_stats(user)))
        return return_data

    @expose('remysmoke.templates.smoke')
    @require(predicates.not_anonymous())
    def smoke(self, **kw):
        """Register a new smoke."""
        if not kw.get('date'):
            kw['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return kw

    @expose()
    @require(predicates.not_anonymous())
    def register_smoke(self, **kw):
        """Try to add the smoking data."""
        error = False
        try:
            parse_date = datetime.strptime(kw['date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            kw['error.date'] = 'Date must be in format YYYY-MM-DD HH:MM:SS'
            error = True

        if kw.get('nosmoke'):
            # This is a nonsmoking event
            # Sanity Check: unsmoke should not occurr on a day with a
            # registered smoke, or on a day with and existing unsmoke.
            today = parse_date.date()
            tomorrow = today + timedelta(days=1)

            unsmoke = DBSession.query(Unsmoke.date) \
                .filter_by(user=request.identity['repoze.who.userid']) \
                .filter_by(date=today).all()
            smoke = DBSession.query(Cigarette.date) \
                .filter_by(user=request.identity['repoze.who.userid']) \
                .filter(Cigarette.date.between(today, tomorrow)).all()
            if smoke:
                flash("You already registered a smoke for {}".format(today), 'error')
                redirect('/smoke', params=kw)
            elif unsmoke:
                flash("You already marked {} as a non-smoking day.".format(today), 'info')
                redirect('/smoke', params=kw)
            else:
                smoke_data = Unsmoke()
                smoke_data.date = parse_date.date()
        else:
            # If there exists an unsmoke for today, probably best to delete it?
            unsmoke = DBSession.query(Unsmoke) \
                .filter_by(user=request.identity['repoze.who.userid']) \
                .filter_by(date=parse_date.date()).all()
            for event in unsmoke:
                DBSession.delete(event)
            DBSession.flush()

            smoke_data = Cigarette()
            smoke_data.date = parse_date
            smoke_data.submit_date = datetime.now()
            if kw['justification']:
                smoke_data.justification = kw['justification']
            else:
                kw['error.justification'] = 'justification is required'
                error = True

        if not error:
            smoke_data.user = request.identity['repoze.who.userid']
            DBSession.add(smoke_data)
            redirect('/')
        else:
            redirect('/smoke', params=kw)

    @expose('remysmoke.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(api_key=facebook_api, login_counter=str(login_counter), came_from=came_from)

    @expose()
    @require(predicates.not_anonymous())
    def user_control(self, public=False):
        request.identity['user'].public=bool(public)
        redirect('/login')

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        user_name = request.identity['user'].display_name
        flash(_('Welcome back, %s!') % user_name)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
