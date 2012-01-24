# -*- coding: utf-8 -*-
"""Main Controller"""

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
        return dict(page='index')

    @expose('remysmoke.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('remysmoke.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('remysmoke.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)
    @expose('remysmoke.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('remysmoke.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

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
