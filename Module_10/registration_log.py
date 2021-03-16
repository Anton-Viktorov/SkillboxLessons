# -*- coding: utf-8 -*-
import logging


def name_valid(name):
    # TO DO: найди встроенную функцию для проверки "что строка состот только из букв".
    #  по идее она будет в документации где-то рядом с isdigit.
    if not name.isalpha():
        raise ValueError(f'Недопустимый символ в имени пользователя: {name}')


def email_valid(m):
    symbol = set('@.')
    if not symbol.issubset(m):
        raise ValueError(f'Некорректный email: {m}')


def age_valid(age):

    age = int(age)  # Знаю, что может выпасть ValueError. Сделано с расчетом поймать его в общем обработчике.
    if 10 > age > 99:
        raise ValueError(f'Некоррекнтый возраст: {age}')


class Logger:
    """Логгер для записи результатов обработки строк"""

    def __init__(self, name, lvl, f_name):
        self.lvl = lvl
        self.filename = f_name
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.lvl)

        logger_handler = logging.FileHandler(self.filename)  # registrations_good.log registrations_bad.log
        self.logger.setLevel(self.lvl)

        logging_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        logger_handler.setFormatter(logging_formatter)

        self.logger.addHandler(logger_handler)

    def add_entry(self, msg):
        if self.lvl == logging.INFO:
            self.logger.info(msg)
        elif self.lvl == logging.ERROR:
            self.logger.error(msg)


good_logger = Logger(lvl=logging.INFO, f_name='registrations_good.log', name='good_logger')
bad_logger = Logger(lvl=logging.ERROR, f_name='registrations_bad.log', name='bad_logger')

exc = (ValueError, ZeroDivisionError, NameError,)

filename = 'registrations.txt'
with open(filename, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            name, email, age = line.split(' ')
            name_valid(name)
            email_valid(email)
            age_valid(age)
        # TO DO: добавь поддержку исключения ZeroDivision и еще какого-нибудь. (просто так, знаю, что они не выпадут)
        #  как упростить запись ниже?

        # Закинуть исключения в кортеж?
        except exc as e:
            bad_logger.add_entry(e)
        else:
            good_logger.add_entry(line)
        finally:
            print(f'Обработал строку: {line}')


# class GoodLogger(Logger):
#     """Логгер для записи корректных данных"""
#
#     def __init__(self):
#         super().__init__(lvl=logging.INFO, f_name='registrations_good.log', name='good_logger')
#
#     def add_entry(self, msg):
#         self.logger.info(msg)
#
#
# class BadLogger(Logger):
#     """Логгер для записи ошибок"""
#
#     def __init__(self):
#         super().__init__(lvl=logging.ERROR, f_name='registrations_bad.log', name='bad_logger')
#
#     def add_entry(self, msg):
#         self.logger.error(msg)

# TO DO: объемненько выходит.
#  Как насчет здесь сделать метод add_entry, который в зависимости от уровня будет добавлять сообщение,
#  в нужное место.
#  .
#  Тогда можно будет создать сколько угодно логгеров: и бэд, и гуд, и не очень гуд. Какие угодно.

#  Изначально сделал два метода для класса родителя. Но подумал, что лучше сделать классы-наследники с одинаковым
#  названием метода для удобства.

# TO DO: например, logging.INFO - уровень ошибки

# TO DO: уф.
#  Два почти одинаковых класса? Есть такая штука - параметры. Используй!

# TO DO: сделай 1 обработчик для кортежа исключений.

# TO DO: например, logging.INFO - уровень ошибки

# TO DO: второму параметру не обязательно быть множество. Он может быть и строкой.

# TO DO: вот это стремный момент. Мы выше затерли переменную m, а тут мы ее как бы восстанавливаем.
#  А еще: множества не хранят порядок. Поэтому восстановленный m скорее всего будет отличаться порядком

# TO DO: можно оба условия объединить через and
# TO DO: выше бы обращаемся к age как к строке. А здесь уже как к int. Непорядок! Так это строка или число?

# class NotNameError(Exception):
#     """Ошибка в имени пользователя"""
#
#     def __init__(self, smb):
#         self.smb = smb
#
#     def __str__(self):
#         return str(self.smb)
#
# TO DO: раз уж мы создали исключение. и даже написали коммент "Ошибка в имени пользователя"
#  может тогда захардкодим сообщение об ошибке в __str__?
#
#
# class NotEmailError(Exception):
#     """Ошибка в почте пользователя"""
#
#     def __init__(self, email):
#         self.email = email
#
#     def __str__(self):
#         return self.email
