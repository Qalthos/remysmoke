"""Smoke Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDateTimePicker, TextArea


class SmokeForm(TableForm):

    class fields(WidgetsList):
        date = CalendarDateTimePicker()
        justification = TextArea()


register_smoke_form = SmokeForm('register_smoke_form', action='register_smoke')
