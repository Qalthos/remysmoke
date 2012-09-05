"""Smoke Form"""

from datetime import datetime

from tw2.forms import FormPage, ListForm, CalendarDateTimePicker, TextArea
from tw2.core import DateTimeValidator, Required


class SmokeForm(FormPage):
    title = ''
    class child(ListForm):
        action = '/register_smoke'
        date = CalendarDateTimePicker(value=datetime.now())
        justification = TextArea(validator=Required)
