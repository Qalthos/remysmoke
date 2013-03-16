# -*- coding: utf-8 -*-
"""Main Controller"""

from datetime import datetime

from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from tgext.mobilemiddleware import expose_mobile
from errorcats.error import ErrorController

from remysmoke.lib.base import BaseController
from remysmoke import model
from remysmoke.model import DBSession
from remysmoke.model.smoke import Cigarette
from remysmoke.widgets import punch_chart, smoke_stats, time_chart
from remysmoke.widgets.smoke import SmokeForm

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
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    error = ErrorController()

    @expose('remysmoke.templates.index')
    @expose_mobile('remysmoke.templates.mobile_index')
    def index(self):
        """Handle the front-page."""
        return dict()

    @expose('remysmoke.templates.widget')
    def week(self):
        """Show cigarettes smoked per week (daily)."""
        return dict(widget=time_chart(1))

    @expose('remysmoke.templates.widget')
    def month(self):
        """Show cigarettes smoked per month (daily)."""
        return dict(widget=time_chart(4))

    @expose('remysmoke.templates.widget')
    def year(self):
        """Show cigarettes smoked per year (weekly)."""
        return dict(widget=time_chart(52, 7))

    @expose('remysmoke.templates.multichart')
    def punch(self):
        return dict(charts=punch_chart())

    @expose('remysmoke.templates.stats')
    def stats(self):
        """Show some stats about cigarette consumption."""
        return dict(data=smoke_stats())

    @expose('remysmoke.templates.widget')
    @expose_mobile('remysmoke.templates.mobile_widget')
    @require(predicates.has_permission('smoke', msg=l_('Only for smokers')))
    def smoke(self, **kw):
        """Register a new smoke."""
        return dict(widget=SmokeForm.display())

    @validate(SmokeForm, error_handler=smoke)
    @expose()
    @require(predicates.has_permission('smoke', msg=l_('Only for smokers')))
    def register_smoke(self, **kw):
        """Try to add the smoking data."""
        smoke_data = Cigarette()
        smoke_data.date = kw['date']
        smoke_data.submit_date = datetime.now()
        smoke_data.user = request.identity['repoze.who.userid']
        smoke_data.justification = kw['justification']
        DBSession.add(smoke_data)
        redirect('/')

    @expose('remysmoke.templates.login')
    @expose_mobile('remysmoke.templates.mobile_login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(login_counter=str(login_counter), came_from=came_from)

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
