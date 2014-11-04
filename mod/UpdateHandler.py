#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from sqlalchemy.sql import and_
from sqlalchemy.orm.exc import NoResultFound
from models.user import User
from check_password import check_password

class UpdateHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('''<form method="post">
                        <p>更新用户信息（留空不变动）</p>
                        <p>cardnum(*)         <input type="text" name="cardnum"></p>
                        <p>number(-)          <input type="text" name="number"></p>
                        <p>password(*)        <input type="password" name="password"></p>
                        <p>pe_password(-)     <input type="password" name="pe_password"></p>
                        <p>lib_username(-)    <input type="text" name="lib_username"></p>
                        <p>lib_password(-)    <input type="password" name="lib_password"></p>
                        <p>card_query_pwd  <input type="password" name="card_query_pwd"></p>
                        <p>card_consume_pwd<input type="password" name="card_consume_pwd"></p>
                        <p><input type="submit" name="submit"></p>
                    </form>''')
        self.write('Herald Auth.')
        self.finish()

    def post(self):
        cardnum = self.get_argument('cardnum', default = '')
        number = self.get_argument('number', default='')
        password = self.get_argument('password', default='')
        pe_password = self.get_argument('pe_password', default='')
        lib_username = self.get_argument('lib_username', default='')
        lib_password = self.get_argument('lib_password', default='')
        card_query_pwd = self.get_argument('card_query_pwd', default='')
        card_consume_pwd = self.get_argument('card_consume_pwd', default='')

        if not (cardnum and password):
            raise tornado.web.HTTPError(400)

        try:
            user = self.db.query(User).filter(
                User.cardnum == cardnum).one()
            if user.password == password or check_password(cardnum, password):
                if number:
                    user.number = number
                if password:
                    user.password = password
                if pe_password:
                    user.pe_password = pe_password
                if lib_username:
                    user.lib_username = lib_username
                if lib_password:
                    user.lib_password = lib_password
                if card_query_pwd:
                    user.card_query_pwd = card_query_pwd
                if card_consume_pwd:
                    user.card_consume_pwd = card_consume_pwd

                self.db.add(user)
                self.db.commit()

                self.write('OK')
                self.db.close()
                self.finish()
            else:
                raise tornado.web.HTTPError(401)
        except NoResultFound:
            if check_password(cardnum, password):
                user = User(cardnum=cardnum, password=password, state=1)
                if number:
                    user.number = number
                if pe_password:
                    user.pe_password = pe_password
                if lib_username:
                    user.lib_username = lib_username
                if lib_password:
                    user.lib_password = lib_password
                if card_query_pwd:
                    user.card_query_pwd = card_query_pwd
                if card_consume_pwd:
                    user.card_consume_pwd = card_consume_pwd
                self.db.add(user)
                self.db.commit()

                self.write('OK')
                self.db.close()
                self.finish()
            else:
                raise tornado.web.HTTPError(401)