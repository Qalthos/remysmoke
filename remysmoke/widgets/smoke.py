"""Smoke Form"""

from datetime import datetime

from tw2.forms import FormPage, ListForm, CalendarDateTimePicker, TextArea
from tw2.core import DateTimeValidator, Required


class SmokeForm(FormPage):
    title = ''
    class child(ListForm):
        action = '/register_smoke'
        date = CalendarDateTimePicker(required=True)
        justification = TextArea(validator=Required)
