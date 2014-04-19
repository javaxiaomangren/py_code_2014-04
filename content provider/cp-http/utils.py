#!/usr/bin/env python
#coding: utf-8

import traceback
import smtplib


def notify_me(func):
    """send a email where exceptions occur"""

    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            _sendmail("message==>%s\n\n\nHost Info:%s " % (traceback.format_exc(), "save deep and rti"),
                      'Exception When Run Function %s' % func.func_name)

    return wrapped


def _sendmail(msg='', subject=''):
    """send a email with msg and subject
    :param msg:
    :param subject:
    """
    to = 'yang.hua@autonavi.com'
    frm_user = 'ixdba_tuan800@163.com'
    frm_passwd = 'tgxstbbA201'

    # smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver = smtplib.SMTP("smtp.163.com", 25)

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(frm_user, frm_passwd)
    header = 'To:%s\nFrom:%s\nSubject:%s\n' % (to, frm_user, subject)
    message = header + '\n %s\n\n' % msg
    smtpserver.sendmail(frm_user, to, message)
    smtpserver.close()

