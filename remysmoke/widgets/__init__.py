from __future__ import print_function, unicode_literals

from datetime import date, datetime, timedelta

import collections
import difflib
import random

from pygal import Config, Dot, DateY
from pygal.style import Style

from remysmoke.model import DBSession
from remysmoke.model.auth import User
from remysmoke.model.smoke import Cigarette

LightStyle = Style(
    background='transparent',
    plot_background='transparent',
    foreground='rgba(0, 0, 0, 0.7)',
    foreground_light='rgb(0, 0, 0)',
    foreground_dark='rgb(238,238,238)',
    colors=('rgb(31, 119, 180)', '#9f6767', '#92ac68',
            '#d0d293', '#9aacc3', '#bb77a4',
            '#77bbb5', '#777777')
)
class BaseConfig(Config):
    def __init__(self, *a, **kw):
        super(BaseConfig, self).__init__(*a, **kw)
        self.width, self.height = (900, 225)
        self.show_dots = False
        self.print_values = False
        self.style = LightStyle
        self.no_prefix = True
        self.disable_xml_declaration = True
        self.include_x_axis = True
        self.js = []


class LineConfig(BaseConfig):
    def __init__(self, *a, **kw):
        super(LineConfig, self).__init__(*a, **kw)
        self.x_label_rotation = 20
        self.order_min = 0
        self.fill = False


def punch_chart():
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

        chart = Dot(BaseConfig())
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for dow in days:
            chart.add(dow, chart_data[dow])
        charts[name] = chart.render(is_unicode=True)


    return charts

def smoke_stats():
    smoke_users = DBSession.query(Cigarette.user).group_by(Cigarette.user).all()
    data = {}
    now = datetime.today()
    for (user,) in smoke_users:
        smoke_data = DBSession.query(Cigarette).filter_by(user=user) \
                              .order_by(Cigarette.date)
        year = smoke_data.filter(Cigarette.date >= now - timedelta(days=365)).all()
        month = smoke_data.filter(Cigarette.date >= now - timedelta(days=28)).all()
        week = smoke_data.filter(Cigarette.date >= now - timedelta(days=7)).all()
        smoke_data = smoke_data.all()
        (user,) = DBSession.query(User.display_name).filter_by(user_name=user).one()

        newest_data = now - smoke_data[-1].date
        oldest_data = now

        streak = timedelta()
        last = smoke_data[0].date

        for datum in smoke_data:
            if oldest_data > datum.date:
                oldest_data = datum.date
            if datum.date - last > streak:
                streak = datum.date - last
            last = datum.date

        excuses = [(smoke_point.justification,
                    smoke_point.date.strftime('%d %b %Y %H:%M'))
                   for smoke_point in smoke_data]
        latest_excuses = reversed(excuses[-5:])
        random_excuses = random.sample(excuses, 5 if len(excuses) >= 5 else len(excuses))

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
        score = smoke_score(smoke_data, timespan)
        dpp = 1.0 * timespan * 20 / len(smoke_data)
        cpm = len(smoke_data) * 10.50 * 30 / (20 * timespan)
        data[user] = dict(score=score, lifespan=dpp, cost=cpm,
                          now=newest_data, best=streak, top=top_excuses,
                          latest=latest_excuses, random=random_excuses)

    return data

def smoke_score(smoke_data, timespan):
    """Takes smoking stats and reduces those stats to a number."""
    delta = 0
    for datum in smoke_data:
        # Score is reduced by 1 for each hour difference
        # Indulgences count as negative too
        #delta += abs(datum.date - datum.submit_date).total_seconds() / 3600.
        this_delta = abs(datum.date - datum.submit_date)
        delta += this_delta.seconds / 3600. + this_delta.days / 24.

    # Score is [days of history] / [# of smokes] - delta
    score = 24.0 * timespan / len(smoke_data) - delta
    return score

def time_chart(weeks, period=1):
    """Get information from a specified interval."""

    date_range = weeks * 7 / period
    period = timedelta(days=period)

    # 'now' is technically tomorrow at 0:00, so that today's smokes have
    # somewhere to go.
    now = date.today() + timedelta(days=1)
    past = now - timedelta(weeks=weeks)
    users = DBSession.query(Cigarette.user).group_by(Cigarette.user).all()
    users_data = {}

    for (user,) in users:
        data = DBSession.query(Cigarette).filter_by(user=user) \
                        .filter(Cigarette.date >= past).all()
        (user,) = DBSession.query(User.display_name) \
                           .filter_by(user_name=user).one()

        # pre-fill the dictionary with zeroes
        freq_data = {(past + x*period): 0 for x in range(date_range)}
        for datum in data:
            distance = (datum.date.date() - past).total_seconds() // period.total_seconds()
            freq_data[past + (int(distance) * period)] += 1

        users_data[user] = freq_data

    if not users_data:
        chart = 'No data to display.'
    else:
        chart = DateY(LineConfig())
        contents = users_data.items()
        for (name, user_data) in contents:
            chart.add(name, sorted(user_data.items()))
            chart = chart.render(is_unicode=True)
    return chart
