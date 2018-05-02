# -*- coding: utf-8 -*-

import os
from datetime import datetime
# import logging
import bs4
import re
import urllib2
import wiks_comm
import db_proxies
import creds


db = db_proxies.DeBe()


def only_value(key, default=None):
    """
    pobierz z settings-DB i zwróć tylko wartość, jeśli nie występuje
    to zwróć default i taką też wpisz do DB
    :param key:
    :return:
    """
    ret = default
    res = db.get_value_for_key(key)
    if res and 'value' in res:
        ret = res['value']
    elif default is not None:
        db.set_value_for_key(key, default)
    return ret


def main():
    """
    wykonuj pętlę główną programu (może trwać nawet 30sekund na jedno proxy, 50 minut na 100sztuk)
    wyniki są w DB, ustaw dostęp do DB w pliku creds_pattern.py i zmień jego nazwę na creds.py
    :return:
    """
    db.set_value_for_key('start', datetime.now())
    # print only_value('start')

    # -------- settings -------

    mytimeout = int(only_value('mytimeout', 30))
    url_to_test = only_value('url_ip', creds.SETTINGS['url_ip'])
    ip_looking_for = only_value('look_for_ip', creds.SETTINGS['look_for_ip'])

    # ------- go!

    wtdog_key = 'proxy_check'
    log_main = wiks_comm.setup_logger('main', os.path.join('./log', 'debug.log'))  # , logging.DEBUG)
    log_main.info(u'running ' + unicode(wtdog_key) + u' ...')

    log_main.info(u'checking IP machine is: %s', url_to_test)
    log_main.info(u'checking timeout is: %s', mytimeout)
    log_main.info(u'looking for IP: %s', ip_looking_for)

    count_to_check = -1
    while count_to_check:

        res = db.get_number_of_not_tested_proxy()
        count_to_check = 0
        if res and 'count_1' in res:
            count_to_check = res['count_1']
            db.set_value_for_key('count_to_check', count_to_check)

        success = False
        hiddedip = None
        page = None
        httpProxy = None
        timestart = datetime.now()
        try:
            ua = db.get_one_random_user_agent()
            log_main.debug(u'random pick one UserAgent: %s', ua)
            webbrowser_headers = ('User-agent', ua)
            httpProxy = db.get_one_random_proxy()  # {'ipaddress': u'53.149.171.103', 'port': 3128L}
            log_main.debug(u'random pick one httpProxy from DB: %s', httpProxy)
            ipport = 'http://' + httpProxy['ipaddress'] + ':' + str(httpProxy['port'])
            log_main.info(u'testing proxy: %s  --> (to check left %s proxies)', ipport, count_to_check)
            proxyHandler = urllib2.ProxyHandler({'http': ipport})
            proxyOpener = urllib2.build_opener(proxyHandler)
            urllib2.install_opener(proxyOpener)
            opener = urllib2.build_opener(proxyHandler)
            urllib2.install_opener(opener)
            opener.addheaders = [webbrowser_headers]
            response = opener.open(url_to_test,
                                   timeout=mytimeout)
            page = response.read()
            timeout = (datetime.now() - timestart).total_seconds()
            log_main.info(u'read PAGE, time: %s', timeout)
        except Exception, e:
            timeout = (datetime.now() - timestart).total_seconds()
            log_main.warning(u'PAGE doesn`t read (time: %s ), error: %s', timeout, e)
            db.put_proxy_exception2(httpProxy, e, timeout)
        if page:
            soup = bs4.BeautifulSoup(page, "lxml")
            if soup:
                success = True
            log_main.debug(u'soup: %s', unicode(soup))
            hiddedip = 1  # ok, nie było mojego IP a więc zostało ukryte
            resu = soup(text=re.compile(ip_looking_for))
            if resu and len(resu) >= 1:
                hiddedip = 0  # nie ukrył --> lipa
                log_main.info(u'my IP was found :-( ')
            else:
                # check for something known on page
                resu2 = soup(text=re.compile(u'wiks'))
                if resu2 and len(resu2) >= 1:
                    log_main.info(u'an expected phrase is found and no my IP-addr. here :-) ')
                else:
                    log_main.info(u'there wasn`t expected phrase on page')
                    success = False
        db.put_result(success, httpProxy, timeout, hiddedip)


if __name__ == "__main__":

    print ('start')
    main()
