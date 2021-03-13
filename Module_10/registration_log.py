# -*- coding: utf-8 -*-
import logging


class NotNameError(Exception):
    """Ошибка в имени пользователя"""

    def __init__(self, smb):
        self.smb = smb

    def __str__(self):
        return str(self.smb)


class NotEmailError(Exception):
    """Ошибка в почте пользователя"""

    def __init__(self, email):
        self.email = email

    def __str__(self):
        return self.email


def name_valid(name):
    symbol = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦШЩЪЪЫЬЭЮЯЧ')
    smb = set(name).difference(symbol)
    if smb:
        raise NotNameError(smb)


def email_valid(m):
    symbol = set('@.')
    m = set(m)
    if not symbol.issubset(m):
        m = ''.join(map(str, m))
        raise NotEmailError(m)


def age_valid(age):
    if not age.isdigit():
        raise ValueError
    if 10 > age > 99:
        raise ValueError


class GoodLogger:
    """Логгер для записи прошедших валидацию аккаунтов"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        logger_handler = logging.FileHandler('registrations_good.log')
        self.logger.setLevel(logging.INFO)

        logging_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        logger_handler.setFormatter(logging_formatter)

        self.logger.addHandler(logger_handler)

    def add_entry(self, msg):
        self.logger.info(msg)


class BadLogger:
    """Логгер для записи ошибок"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

        logger_handler = logging.FileHandler('registrations_bad.log')
        self.logger.setLevel(logging.ERROR)

        logging_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        logger_handler.setFormatter(logging_formatter)

        self.logger.addHandler(logger_handler)

    def add_entry(self, msg):
        self.logger.error(msg)


good_log = GoodLogger()
bad_log = BadLogger()


filename = 'registrations.txt'
with open(filename, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            name, email, age = line.split(' ')
            name_valid(name)
            email_valid(email)
        except ValueError as e:
            bad_log.add_entry(e)
        except NotNameError as e:
            bad_log.add_entry(e)
        except NotEmailError as e:
            bad_log.add_entry(e)
        else:
            good_log.add_entry(line)
