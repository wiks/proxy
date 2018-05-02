# -*- coding: utf-8 -*-

# import os
# import sys
# import random
# import time
# import logging
# import logging.handlers
# import os
from sqlalchemy import schema, create_engine, Column, Table, Integer, UnicodeText, String, types, Time, Boolean, Text, Float
from sqlalchemy import select, update, and_, delete, or_, cast, Date, func, insert
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.mysql import BIGINT
# from sqlalchemy import exc
from datetime import datetime  # , timedelta, date
# import logging
# import httplib
# import urllib2
# import db_settings_local
import db_comm_class
# from wiks_py import wiks_comm
import creds


class DeBe(db_comm_class.DeBeComm):

    __doc__ = '''ver.
    klasa dla bazy danych MySQL
    '''

    def __init__(self, path_for_create_engine_db=None):
        """

        :param path_for_create_engine_db:
        """
        # self.dbname = 'wiks_bot'  # określone w settings
        # self.tbl_prefix = ''
        self.col_id_name = 'id'

        # self.text_len_limit = 2 ^ 16 - 1
        # https://dev.mysql.com/doc/refman/5.7/en/storage-requirements.html
        # BLOB, TEXT               L + 2 bytes, where L < 2^16   (64 Kibibytes)

        metadata = schema.MetaData()
        if not path_for_create_engine_db:
            path_for_create_engine_db = str(URL(**creds.DATABASE_PROXY))
        self.db = create_engine(path_for_create_engine_db + '?charset=utf8',
                                pool_pre_ping=True)
        self.db.echo = False  # True  #
        self.db.encoding = 'utf-8'
        metadata.bind = self.db

        # self.tab_all = Table('all', metadata,
        #                      autoload=True,
        #                      autoload_with=self.db
        #                      )
        self.tab_all = Table('all', metadata,
                             Column('id', Integer, primary_key=True),
                             Column('ipaddress', String(20), nullable=True, default=None),
                             Column('port', Integer, nullable=True, default=None),
                             Column('country', String(30), nullable=True, default=None),
                             Column('dt_put', types.TIMESTAMP(), nullable=True, default=None),
                             Column('last_dt_success', types.TIMESTAMP(), nullable=True, default=None),
                             Column('last_success_time', Integer, nullable=True, default=None),
                             Column('last_dt_porage', types.TIMESTAMP(), nullable=True, default=None),
                             Column('turnoff', Integer, nullable=True, default=None),
                             Column('hiddedip', Integer, nullable=True, default=None),
                             mysql_collate='utf8_general_ci'
                             )
        # self.proxy_exceptions = Table('proxy_exceptions', metadata,
        #                               autoload=True,
        #                               autoload_with=self.db
        #                               )
        self.proxy_exceptions = Table('proxy_exceptions', metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('ipaddress', String(20), nullable=True, default=None),
                                      Column('port', Integer, nullable=True, default=None),
                                      Column('id_exception', Integer, nullable=True, default=None),
                                      Column('timeout', Float, nullable=True, default=None),
                                      Column('dt', types.TIMESTAMP(), nullable=True, default=None),
                                      mysql_collate='utf8_general_ci'
                                      )
        # self.proxy_kind_exceptions = Table('proxy_kind_exceptions', metadata,
        #                               autoload=True,
        #                               autoload_with=self.db
        #                               )
        self.proxy_kind_exceptions = Table('proxy_kind_exceptions', metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('exception', String(200), nullable=True, default=None),
                                      Column('dt', types.TIMESTAMP(), nullable=True, default=None),
                                      mysql_collate='utf8_general_ci'
                                      )
        # self.tab_webbrowser_headers = Table('webbrowser_headers', metadata,
        #                                     autoload=True,
        #                                     autoload_with=self.db
        #                                     )
        self.tab_webbrowser_headers = Table('webbrowser_headers', metadata,
                                            Column('id', Integer, primary_key=True),
                                            Column('user_agent', String(200), nullable=True, default=None),
                                            Column('turnoff', Integer, nullable=True, default=None),
                                            mysql_collate='utf8_general_ci'
                                            )
        # self.tab_keyval = Table('keyval', metadata,
        #                         autoload=True,
        #                         autoload_with=self.db
        #                         )
        self.tab_keyval = Table('keyval', metadata,
                                Column('id', Integer, primary_key=True),
                                Column('key', String(20), nullable=True, default=None),
                                Column('value', String(50), nullable=True, default=None),
                                Column('dt', types.TIMESTAMP(), nullable=True, default=None),
                                mysql_collate='utf8_general_ci'
                                )
        metadata.create_all(checkfirst=True)

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.db.dispose()

    def set_value_for_key(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        self.setupdate_key_value2(self.tab_keyval, key, None, value, self.db)
        return None

    def get_value_for_key(self, key):
        """

        :param key:
        :param value:
        :return:
        """
        ret = self.get_value_dt_4key2(self.tab_keyval, key, None, self.db)
        return ret

    def put_new_proxy_if_not_in_db(self, ip, port, country_id, country):
        """
        sprawdź, czy IP+port w DB, jeśli nie to umieść ją w niej
        :param ip:
        :param port:
        :param country_id:
        :param country:
        :return:
        """
        co = country_id + u':' + country
        varunek = and_(self.tab_all.c.ipaddress == ip,
                       self.tab_all.c.port == port
                       )
        sel = select([self.tab_all.c.id],
                     varunek
                     ).limit(1)
        rows = self.execute_select_ret_list_of_dict2(self.db, sel)
        if not rows:
            ins = self.tab_all.insert(values=dict(ipaddress=ip,
                                                  port=port,
                                                  country=co,
                                                  dt_put=datetime.now()))

            self.db.execute(ins)
        return None

    def get_one_random_user_agent(self):
        """
        pobierz losowo jeden useragent
        :return:
        """
        ret = u'Mozilla/5.0'
        sel = select([self.tab_webbrowser_headers.c.user_agent],
                     self.tab_webbrowser_headers.c.turnoff == 0
                     ).order_by(func.rand()).limit(1)
        row = self.execute_select_ret_onerow_dict2(self.db, sel)
        if row:
            ret = row['user_agent']
        return ret

    def get_one_random_proxy(self):
        """

        :return:
        """
        ret = None
        sel = select([self.tab_all.c.ipaddress,
                      self.tab_all.c.port],
                     and_(self.tab_all.c.turnoff == 0,
                          self.tab_all.c.last_dt_success == None,  # \jeszcze nie sprawdzane
                          # self.tab_all.c.last_dt_porage == None    # /
                          )
                     ).order_by(func.rand()).limit(1)
        row = self.execute_select_ret_onerow_dict2(self.db, sel)
        if row:
            ret = row
            # print row  # {'ipaddress': u'53.149.171.103', 'port': 3128L}
        return ret

    def get_one_random_proxy0(self):
        """

        :return:
        """
        ret = None
        sel = select([self.tab_all.c.ipaddress,
                      self.tab_all.c.port],
                     and_(self.tab_all.c.turnoff == 0,
                          self.tab_all.c.last_dt_success == None,  # \jeszcze nie sprawdzane
                          self.tab_all.c.last_dt_porage == None    # /
                          )
                     ).order_by(func.rand()).limit(1)
        row = self.execute_select_ret_onerow_dict2(self.db, sel)
        if row:
            ret = row
            # print row  # {'ipaddress': u'53.149.171.103', 'port': 3128L}
        return ret

    def get_number_of_not_tested_proxy(self):
        """

        :return:
        """
        ret = None
        sel = select([func.count()],
                     and_(self.tab_all.c.turnoff == 0,
                          self.tab_all.c.last_dt_success == None,  # \jeszcze nie sprawdzane
                          # self.tab_all.c.last_dt_porage == None    # /
                          )
                     )
        row = self.execute_select_ret_onerow_dict2(self.db, sel)
        if row:
            ret = row
            # print row  # {'ipaddress': u'53.149.171.103', 'port': 3128L}
        return ret

    def put_ipport_proxy_success(self, httpProxy, timeout, hiddedip=None):
        """
        zaznacz, że sukces i jaki czas, hiddedip = 1 --> w wyniku nie było mojego IP
        :param ip:        :param port:
        :param timeout:
        :return:
        """
        if httpProxy and 'ipaddress' in httpProxy and 'port' in httpProxy:
            upd = update(self.tab_all,
                         and_(self.tab_all.c.ipaddress == httpProxy['ipaddress'],
                              self.tab_all.c.port == httpProxy['port'])
                         )
            self.db.execute(upd,
                            last_dt_success=datetime.now(),
                            last_success_time=timeout,
                            )
            if hiddedip is not None:
                self.db.execute(upd,
                                hiddedip=hiddedip,
                                )
        return None

    def put_ipport_proxy_porage(self, httpProxy):
        """
        zaznacz, że sukces i jaki czas
        :param ip:
        :param port:
        :param timeout:
        :return:
        """
        if httpProxy and 'ipaddress' in httpProxy and 'port' in httpProxy:
            upd = update(self.tab_all,
                         and_(self.tab_all.c.ipaddress == httpProxy['ipaddress'],
                              self.tab_all.c.port == httpProxy['port'])
                         )
            self.db.execute(upd,
                            last_dt_porage=datetime.now(),
                            )
        return None

    # def open_read_page(self, url_to_test, mytimeout=30):
    #     """
    #
    #     :param url_to_test:
    #     :return:
    #     """
    #     page = None
    #     httpProxy = None
    #     timestart = datetime.now()
    #     try:
    #         webbrowser_headers = ('User-agent', self.get_one_random_user_agent())
    #         print webbrowser_headers
    #         httpProxy = self.get_one_random_proxy()  # {'ipaddress': u'53.149.171.103', 'port': 3128L}
    #         print httpProxy
    #
    #         proxyHandler = urllib2.ProxyHandler(
    #             {'http': 'http://' + httpProxy['ipaddress'] + ':' + str(httpProxy['port'])})
    #         proxyOpener = urllib2.build_opener(proxyHandler)
    #         urllib2.install_opener(proxyOpener)
    #
    #         opener = urllib2.build_opener(proxyHandler)
    #         urllib2.install_opener(opener)
    #         opener.addheaders = [webbrowser_headers]
    #         response = opener.open(url_to_test,
    #                                timeout=mytimeout)
    #         page = response.read()
    #     except Exception, e:
    #         print 'exception:', e
    #         # exception: [Errno 104] Connection reset by peer
    #         # exception: <urlopen error timed out>
    #     timeout = (datetime.now() - timestart).total_seconds()
    #     return page, httpProxy, timeout

    def put_result(self, success, httpProxy, timeout, hiddedip=None):
        """

        :return:
        """
        if success:
            self.put_ipport_proxy_success(httpProxy, timeout, hiddedip)
        else:
            self.put_ipport_proxy_porage(httpProxy)
        return None

    # def put_proxy_exception(self, httpProxy, e, timeout=None):
    #     """
    #     zapamiętaj błąd zwrócony przez proxy
    #     :param httpProxy:
    #     :param timeout:
    #     :return:
    #     """
    #     # ipaddress exception timeout dt
    #     if httpProxy and 'ipaddress' in httpProxy and 'port' in httpProxy:
    #         ins = self.proxy_exceptions.insert(values=dict(ipaddress=httpProxy['ipaddress'],
    #                                                        port=httpProxy['port'],
    #                                                        exception=e,
    #                                                        timeout=timeout,
    #                                                        dt=datetime.now()))
    #         self.db.execute(ins)
    #     return None

    def put_proxy_exception2(self, httpProxy, e, timeout=None):
        """
        zapamiętaj błąd zwrócony przez proxy
        :param httpProxy:
        :param timeout:
        :return:
        """
        # proxy_kind_exceptions

        if httpProxy and 'ipaddress' in httpProxy and 'port' in httpProxy and e:
            sel = select([self.proxy_kind_exceptions.c.id],
                         self.proxy_kind_exceptions.c.exception == e
                         )
            row = self.execute_select_ret_onerow_dict2(self.db, sel)
            if row and 'id' in row:
                id_exception = row['id']
            else:
                ins = self.proxy_kind_exceptions.insert(values=dict(exception=e,
                                                                    dt=datetime.now()))
                res = self.db.execute(ins)
                id_exception = res.lastrowid
            ins = self.proxy_exceptions.insert(values=dict(ipaddress=httpProxy['ipaddress'],
                                                           port=httpProxy['port'],
                                                           id_exception=id_exception,
                                                           timeout=timeout,
                                                           dt=datetime.now()))
            self.db.execute(ins)
        return None

    def clear_ip(self, ip):
        """
        zrób, jakby IP nie był sprawdzany jeszcze
        :param ip:
        :return:
        """
        upd = update(self.tab_all,
                     self.tab_all.c.ipaddress == ip
                     )
        self.db.execute(upd,
                        last_dt_porage=None,
                        last_dt_success=None,
                        last_success_time=None,
                        hiddedip=None,
                        )
        # sel = select([self.tab_all],
        #              and_(self.tab_all.c.ipaddress == ip,
        #                   )
        #              )
        # row = self.execute_select_ret_onerow_dict2(self.db, sel)
        # print row
        return None

    # def popraw_exceptions_stare_na_nowe(self):
    #     """
    #
    #     :return:
    #     """
    #     sel = select([self.proxy_exceptions],
    #                  self.proxy_exceptions.c.id_exception == 0
    #                  )
    #     rows = self.execute_select_ret_list_of_dict2(self.db, sel)
    #     for row1 in rows:
    #         e = row1['exception']
    #         print row1['id'], e
    #         sel = select([self.proxy_kind_exceptions.c.id],
    #                      self.proxy_kind_exceptions.c.exception == e
    #                      )
    #         row2 = self.execute_select_ret_onerow_dict2(self.db, sel)
    #         if row2 and 'id' in row2:
    #             id_exception = row2['id']
    #             print id_exception
    #             upd = update(self.proxy_exceptions,
    #                          self.proxy_exceptions.c.id == row1['id']
    #                          )
    #             self.db.execute(upd,
    #                             id_exception=id_exception
    #                             )



if __name__ == "__main__":

    print 'start'

    db = DeBe()
    # db.popraw_exceptions_stare_na_nowe()
    print 'już'