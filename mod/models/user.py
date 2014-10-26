#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 13:02:58
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import dbengine, Base

class User(Base):
    __tablename__ = 'user'
    cardnum = Column(String(10), primary_key=True)
    number = Column(String(50), nullable=True)
    password = Column(String(50), nullable=False)
    pe_password = Column(String(50), nullable=True)
    lib_username = Column(String(50), nullable=True)
    lib_password = Column(String(50), nullable=True)
    card_query_pwd = Column(String(50), nullable=True)
    card_consume_pwd = Column(String(50), nullable=True)
    state = Column(Integer, nullable=False)
