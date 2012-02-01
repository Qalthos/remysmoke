"""Smoke Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDateTimePicker, TextArea
from tw.forms.validators import NotEmpty


class SmokeForm(TableForm):

    class fields(WidgetsList):
        date = CalendarDateTimePicker()
        justification = TextArea(validator=NotEmpty())


register_smoke_form = SmokeForm('register_smoke_form', action='register_smoke')
