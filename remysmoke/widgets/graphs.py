from __future__ import division, print_function, unicode_literals

from datetime import datetime, timedelta

import collections

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
        self.x_label_rotation = 20


class LineConfig(BaseConfig):
    def __init__(self, *a, **kw):
        super(LineConfig, self).__init__(*a, **kw)
        self.order_min = 0
        self.fill = False


class DotConfig(BaseConfig):
    def __init__(self, *a, **kw):
        super(DotConfig, self).__init__(*a, **kw)
        self.x_labels = ['{0:02d}:00'.format(hour) for hour in range(24)]
        self.show_legend = False
        self.show_x_guides = True
        self.show_y_guides = True


def punch_chart():
    user = DBSession.query(Cigarette.user).group_by(Cigarette.user).one()[0]
    cigarettes = DBSession.query(Cigarette).filter_by(user=user).all()
    (name,) = DBSession.query(User.display_name) \
                       .filter_by(user_name=user).one()

    chart_data = collections.defaultdict(lambda: [0]*24)
    for cigarette in cigarettes:
        dow = cigarette.date.strftime('%A')
        hour = cigarette.date.hour
        chart_data[dow][hour] += 1

    chart = Dot(DotConfig())
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for dow in days:
        chart.add(dow, chart_data[dow])

    return chart.render(is_unicode=True)


def time_chart(weeks, period=1):
    """Get information from a specified interval."""

    date_range = weeks * 7 // period
    period = timedelta(days=period)

    # 'now' is technically tomorrow at 0:00, so that today's smokes have
    # somewhere to go.
    now = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) \
        + timedelta(days=1)
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
            distance = (datum.date - past).total_seconds() // period.total_seconds()
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
