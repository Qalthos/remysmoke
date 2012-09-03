"""Smoke Form"""

from tw2.forms import ListForm, CalendarDateTimePicker, TextArea
from tw2.core import DateTimeValidator, Required


class SmokeForm(ListForm):
    date = CalendarDateTimePicker(validator=DateTimeValidator())
    justification = TextArea(validator=Required)


register_smoke_form = SmokeForm()
