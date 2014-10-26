#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 14:47:25
# @Author  : yml_bright@163.com

import app, user, privilege
from db import dbengine, Base

Base.metadata.create_all(dbengine)