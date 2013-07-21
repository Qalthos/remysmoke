# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime

from remysmoke.model import DeclarativeBase, metadata, DBSession


class Unsmoke(DeclarativeBase):
    __tablename__ = 'unsmoke'

    #{ Columns

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    user = Column(Unicode(255), nullable=False)

    #}
