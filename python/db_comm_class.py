# -*- coding: utf-8 -*-

# /usr/local/lib/python2.7/dist-packages/wiks_py

from sqlalchemy import select, update, delete, and_  #, insert , or_, func
from datetime import datetime  # , timedelta

'''
execute_select_ret_list_of_dict2
execute_select_ret_onerow_dict2
get_value_dt_4key2
setupdate_key_value2
'''


class DeBeComm:

    __doc__ = '''ver. 20180131 2041
    klasa wspólnych metod dla bazy danych\n

    jest o tyle klasą abstrakcyjną, że budowa na niej samej obiektu nie ma sensu
    zakładam, że bazując na niej do każdej z klas DB mogę dziedziczyć execute 3pierwsze,
    zaś te z key-value, będą wymagały ujednolicenia tabel\n

    mysql> describe alert_keyvalue;\n

    **+-------+--------------+------+-----+---------+----------------+**\n
    **| Field | Type         | Null | Key | Default | Extra          |**\n
    **+-------+--------------+------+-----+---------+----------------+**\n
    **| db_id | int(11)      | NO   | PRI | NULL    | auto_increment |**\n
    **| key   | varchar(50)  | YES  |     | NULL    |                |**\n
    **<-- ew. addkey -->**\n
    **| value | varchar(100) | YES  |     | NULL    |                |**\n
    **| dt    | timestamp    | YES  |     | NULL    |                |**\n
    **+-------+--------------+------+-----+---------+----------------+**\n
    '''

    def execute_select_ret_list_of_dict2(self,
                                         db,
                                         sel):
        """
        przygotowaną alchemiczną frazę select execute i zwróć listę dictionaries
        :param db:
        :param sel:
        :return:
        """
        result = db.execute(sel)
        ret = []
        if result.rowcount > 0:
            for row in result:  # "This result object does not return rows. "  # TODO ?????????
                ret.append(dict(row))
        return ret

    def execute_select_ret_onerow_dict2(self,
                                        db,
                                        sel):

        """
        przygotowaną select (np. z limit 1 wykonaj i pobierz pierwszy wiersz do dictionary)
        :param db:
        :param sel:
        :return:
        """
        result = db.execute(sel)
        first_row = {}
        if result.rowcount > 0:
            first_row = dict(result.first())
        return first_row

    def get_value_dt_4key2(self,
                           tbl_key_values,
                           key,
                           addkey=None,
                           db=None):
        """
        ! tam gdzietrzeba wywołać bez DB można w rozszerzającej metodzxie dodać DB jako default
        pobierz wartość i dt
        :param db:
        :param tbl_key_values:
        :param key:
        :param addkey:
        :return:
        """
        where = tbl_key_values.c.key == key
        if addkey:
            where = and_(tbl_key_values.c.key == key,
                         tbl_key_values.c.addkey == addkey)
        sel = select([tbl_key_values.c.value,
                      tbl_key_values.c.dt],
                     where).limit(1)
        result = self.execute_select_ret_onerow_dict2(db,
                                                      sel
                                                      )
        return result

    def _ins(self,
             db,
             tbl_key_values,
             key,
             addkey=None,
             val=datetime.now()
             ):
        """

        :return:
        """
        if addkey:
            ins = tbl_key_values.insert(values=dict(key=key,
                                                    addkey=addkey,
                                                    value=val,
                                                    dt=datetime.now()))
        else:
            ins = tbl_key_values.insert(values=dict(key=key,
                                                    value=val,
                                                    dt=datetime.now()))
        print ins
        db.execute(ins)

    def setupdate_key_value2(self,
                             tbl_key_values,
                             key,
                             addkey=None,
                             val=datetime.now(),
                             db=None):
        """
        w tabeli key-value updatuje wartość dla keya,
        gdy trzeba to wstawia,
        gdy za dużo to kasuje
        :param db:
        :param tbl_key_values:
        :param key:
        :param addkey:
        :param val:
        :return:
        """
        where0 = tbl_key_values.c.key.like(key)
        if addkey:
            where0 = and_(tbl_key_values.c.key.like(key),
                          tbl_key_values.c.addkey == addkey)
        sel = select([tbl_key_values],
                     where0)
        result = db.execute(sel)
        if result.rowcount > 0:
            if result.rowcount == 1:
                upd = update(tbl_key_values,
                             where0)
                db.execute(upd,
                           value=val,
                           dt=datetime.now())
            else:
                dele = delete(tbl_key_values,
                              where0)
                db.execute(dele)
                self._ins(db,
                          tbl_key_values,
                          key,
                          addkey,
                          val)
        else:
            self._ins(db,
                      tbl_key_values,
                      key,
                      addkey,
                      val)
        return None
