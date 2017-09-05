#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:46:36
# @Author  : yml_bright@163.com

import os
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.gen

from mod.models.db import dbengine
from mod.AuthHandler import AuthHandler
from mod.DeauthHandler import DeauthHandler
from mod.CheckHandler import CheckHandler
from mod.UpdateHandler import UpdateHandler
from mod.APIHandler import APIHandler

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

class AuthCenter(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/uc/auth', AuthHandler),
            (r'/uc/deauth', DeauthHandler),
            (r'/uc/check', CheckHandler),
            (r'/uc/update', UpdateHandler),
            (r'/api/([\S]+)', APIHandler),
        ]
        settings = dict(
            cookie_secret="87C0BB001D10FBF11874589E0AC7823F",
            debug=False
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=dbengine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    AuthCenter().listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()
