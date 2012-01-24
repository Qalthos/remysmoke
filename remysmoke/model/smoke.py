# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
#from sqlalchemy.orm import relation, backref

from remysmoke.model import DeclarativeBase, metadata, DBSession


class Cigarette(DeclarativeBase):
    __tablename__ = 'cigarette'

    #{ Columns

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    user = Column(Unicode(255), nullable=True)
    justification = Column(Unicode(255))

    #}
