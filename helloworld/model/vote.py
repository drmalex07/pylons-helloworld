# -*- encoding: utf-8 -*- 

from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relation, relationship, backref

from datetime import datetime;

from helloworld.model.meta import Base

class Vote(Base):
    __table__ = Table ('vote', Base.metadata,
        Column('id', Integer(), primary_key=True),
        Column('vote', Integer, nullable=True),
        Column('email', String(100), nullable=False, index=True),
        Column('description', String(256), nullable=True),
        Column('created_at', DateTime(), nullable=False),
        UniqueConstraint('email'),
    )

    def __init__(self, vote=None, email=None, created_at=None, description=None):
        self.email = email;
        self.vote  = vote;
        self.created_at = created_at or datetime.now();
        self.description = description;

    def __unicode__(self):
        return "<vote %d <%s>>" % (self.vote, self.email)


