# -*- coding: utf-8 -*-
"""Main Controller"""

import collections
from datetime import datetime, timedelta
import difflib
import random
from time import mktime

from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from remysmoke import model
from repoze.what import predicates
from remysmoke.controllers.secure import SecureController
from remysmoke.model import DBSession, metadata
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from tw2.protovis.conventional import LineChart

from remysmoke.lib.base import BaseController
from remysmoke.controllers.error import ErrorController
from remysmoke.model.smoke import Cigarette
from remysmoke.model.auth import User
from remysmoke.widgets.smoke import register_smoke_form
from remysmoke.widgets.punch import Punchcard

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

    @expose('remysmoke.templates.chart')
    def week(self):
        """Show cigarettes smoked per week (daily)."""
        chart = self.time_chart(1)
        return dict(chart=chart)

    @expose('remysmoke.templates.chart')
    def month(self):
        """Show cigarettes smoked per month (daily)."""
        chart = self.time_chart(4)
        return dict(chart=chart)

    @expose('remysmoke.templates.chart')
    def year(self):
        """Show cigarettes smoked per year (weekly)."""
        chart = self.time_chart(52, 7)
        return dict(chart=chart)

    def time_chart(self, weeks, period=1):
        """Get information from a specified interval."""

        frequency = weeks * 7 / period

        # 'now' is technically tomorrow at 0:00, so that today's smokes have
        # somewhere to go.
        now = datetime.today().replace(hour=0, minute=0, second=0,
                                       microsecond=0) + timedelta(days=1)
        past = now - timedelta(weeks=weeks)
        users = DBSession.query(Cigarette.user).group_by(Cigarette.user).all()
        user_data = {}

        for (user,) in users:
            data = DBSession.query(Cigarette).filter_by(user=user) \
                            .filter(Cigarette.date >= past).all()
            (user,) = DBSession.query(User.display_name) \
                               .filter_by(user_name=user).one()

            freq_data = [{'x': mktime((past + timedelta(days=x*period))
                                      .timetuple()) * 1000, 'y': 0}
                         for x in range(frequency)]
            for datum in data:
                delta = (datum.date - past).days / period
                freq_data[delta]['y'] += 1

            user_data[str(user)] = freq_data

        if not user_data:
            chart = 'No data to display.'
        else:
            chart = LineChart(p_data=user_data.values(),
                    p_labels=user_data.keys(), p_time_series=True,
                    p_time_series_format='%m/%d', p_width=900
                ).display()
        return chart

    @expose('remysmoke.templates.multichart')
    def punch(self):
        users = DBSession.query(Cigarette.user).group_by(Cigarette.user).all()
        charts = dict()
        for (user,) in users:
            cigarettes = DBSession.query(Cigarette).filter_by(user=user).all()
            (name,) = DBSession.query(User.display_name) \
                               .filter_by(user_name=user).one()

            chart_data = collections.defaultdict(lambda: [0]*24)
            for cigarette in cigarettes:
                dow = cigarette.date.strftime('%A')
                hour = cigarette.date.hour
                chart_data[dow][hour] += 1

            real_data = []
            for dow, day_data in chart_data.items():
                for x, count in enumerate(day_data):
                    if count:
                        real_data.append(dict(x=x, y=dow, z=count))

            charts[name] = Punchcard(p_data=real_data, p_width=900, p_left=65).display()
        return dict(charts=charts)

    @expose('remysmoke.templates.stats')
    def stats(self):
        """Show some stats about cigarette consumption."""
        smoke_users = DBSession.query(Cigarette.user).group_by(Cigarette.user).all()
        data = {}
        now = datetime.today()
        for (user,) in smoke_users:
            smoke_data = DBSession.query(Cigarette).filter_by(user=user).order_by(Cigarette.date).all()
            (user,) = DBSession.query(User.display_name).filter_by(user_name=user).one()

            newest_data = now - smoke_data[-1].date
            oldest_data = now

            streak = timedelta()
            last = smoke_data[0].date
            delta = timedelta()

            for datum in smoke_data:
                delta += datum.date - datum.submit_date
                if oldest_data > datum.date:
                    oldest_data = datum.date
                if datum.date - last > streak:
                    streak = datum.date - last
                last = datum.date

            excuses = [(smoke_point.justification,
                        smoke_point.date.strftime('%d %b %Y %H:%M'))
                       for smoke_point in smoke_data]
            latest_excuses = reversed(excuses[-5:])
            random_excuses = random.sample(excuses[:-5], 5)

            counts = list()
            for excuse, date in excuses:
                excuse = excuse.lower().strip()
                for merge_pair in counts:
                    if difflib.get_close_matches(excuse, merge_pair[0], 1, .8):
                        if excuse not in merge_pair[0]:
                            merge_pair[0].append(excuse)
                        merge_pair[1] += 1
                        break
                else:
                    counts.append([[excuse], 1])
            top_excuses = sorted([(count, similar) for similar, count
                                  in counts], reverse=True)[:5]

            timespan = max((datetime.today() - oldest_data).days + 1, 1)
            delta = (delta.seconds / 3600.) + (delta.days * 24)
            score = (24.0 / len(smoke_data)) * timespan + delta
            dpp = 1.0 * timespan * 20 / len(smoke_data)
            cpm = len(smoke_data) * 10.50 * 30 / (20 * timespan)
            data[user] = dict(score=score, lifespan=dpp, cost=cpm,
                              now=newest_data, best=streak, top=top_excuses,
                              latest=latest_excuses, random=random_excuses)

        return dict(data=data)

    @expose('remysmoke.templates.form')
    @require(predicates.has_permission('smoke', msg=l_('Only for smokers')))
    def smoke(self, **kw):
        """Register a new smoke."""
        return dict(form=register_smoke_form())

    @validate(register_smoke_form, error_handler=smoke)
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
