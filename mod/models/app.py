#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 13:20:49
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey

from db import dbengine, Base

class Application(Base):
    __tablename__ = 'application'
    aid = Column(Integer, primary_key=True)
    uuid = Column(String(32), nullable=False)
    tag = Column(String(255), nullable=True)
    state = Column(String(1), nullable=False)
        # 1 means app can use api forever
        # 2 means app can use api when access_left > 0
        # [a-z] means app only can use some api
        # [A-Z] means app only can use some api when access_left > 0
    access_left = Column(Integer, default=0)
