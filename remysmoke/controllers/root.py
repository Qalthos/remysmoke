# -*- coding: utf-8 -*-
"""Main Controller"""

from datetime import datetime, timedelta

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from remysmoke import model
from repoze.what import predicates
from remysmoke.controllers.secure import SecureController
from remysmoke.model import DBSession, metadata
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from remysmoke.lib.base import BaseController
from remysmoke.controllers.error import ErrorController
from remysmoke.model.smoke import Cigarette
from remysmoke.widgets.smoke import register_smoke_form

__all__ = ['RootController']


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
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    @expose('remysmoke.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict()

    @expose('remysmoke.templates.week')
    def week(self):
        """Show cigarettes smoked per week (daily)."""
        past = datetime.today() - timedelta(weeks=1)
        data = DBSession.query(Cigarette).filter(Cigarette.date >= past).all()
        final_data = [[] for x in range(7)]
        for datum in data:
            delta = (datum.date - past).days
            final_data[delta].append(datum)
        return dict(data=final_data)

    @expose('remysmoke.templates.month')
    def month(self):
        """Show cigarettes smoked per month (daily)."""
        past = datetime.today() - timedelta(weeks=4)
        data = DBSession.query(Cigarette).filter(Cigarette.date >= past).all()
        final_data = [[] for x in range(31)]
        for datum in data:
            delta = (datum.date - past).days
            final_data[delta].append(datum)
        return dict(data=final_data)

    @expose('remysmoke.templates.year')
    def year(self):
        """Show cigarettes smoked per year (weekly)."""
        past = datetime.today() - timedelta(weeks=52)
        data = DBSession.query(Cigarette).filter(Cigarette.date >= past).all()
        final_data = [[] for x in range(52)]
        for datum in data:
            delta = (datum.date - past).days / 7
            final_data[delta].append(datum)
        return dict(data=final_data)

    @expose('remysmoke.templates.stats')
    def stats(self):
        """Show some stats about cigarette consumption."""
        smoke_users = DBSession.query(Cigarette.user).group_by(Cigarette.user).all()
        data = {}
        for (user,) in smoke_users:
            smoke_data = DBSession.query(Cigarette).filter_by(user=user).all()

            oldest_data = datetime.today()
            for datum in smoke_data:
                if oldest_data > datum.date:
                    oldest_data = datum.date

            timespan = datetime.today() - oldest_data
            spd = 1.0 * len(smoke_data) / timespan.days
            dpp = 1.0 * timespan.days * 20 / len(smoke_data)
            cpm = len(smoke_data) * 10.50 / (20 * timespan.days / 30)
            data[user] = dict(smokes=spd, lifespan=dpp, cost=cpm)

        print data
        return dict(data=data)

    @expose('remysmoke.templates.form')
    #@require(predicates.has_permission('smoke', msg=l_('Only for smokers')))
    def smoke(self, **kw):
        """Register a new smoke."""
        return dict(form=register_smoke_form())

    @expose()
    #@require(predicates.has_permission('smoke', msg=l_('Only for smokers')))
    def register_smoke(self, **kw):
        """Try to add the smoking data."""
        smoke_data = Cigarette()
        smoke_data.date = datetime.strptime(kw['date'], "%Y/%m/%d %H:%M")
        smoke_data.user = request.identity['repoze.who.userid']
        smoke_data.justification = kw['justification']
        DBSession.add(smoke_data)
        redirect('/')

    @expose('remysmoke.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

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
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
