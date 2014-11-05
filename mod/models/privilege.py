#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 13:14:31
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import dbengine, Base

class Privilege(Base):
    __tablename__ = 'privilege'
    uuid = Column(String(40), primary_key=True)
    cardnum = Column(ForeignKey(u'user.cardnum'))
    aid = Column(ForeignKey(u'application.aid'))
    last_access = Column(Integer, nullable=True)
    access_count = Column(Integer, default=0)