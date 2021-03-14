# -*- coding: utf-8 -*-
import random


# Сначала я вообще не понял задание. Думал, что исключение должно выпадать каждый день.
# Акаждому исключению нужно присвоить некий "вес вероятности".
# Даже нашел алгоритм с random.choice(), который учитывает эту вероятность. Но потом походил подумал,
# что что-то не сходится. А потом дошло, что исключение может и не выпасть. И дело пошло)

class IamGodError(Exception):
    pass


class DrunkError(Exception):
    pass


class CarCrashError(Exception):
    pass


class GluttonyError(Exception):
    pass


class DepressionError(Exception):
    pass


class SuicideError(Exception):
    pass


# Список из 13 возможных событий
# TODO:
#  1. пусть будут только исключени;
#  2. лучше кортеж использовать, если список не собираемся модицифировать.
#       Кортежи полезны в 2х случаях:
#           1. список-константа;
#           2. для хранения полей одной сущности. Например: список предметов в универе:
#               [('матан', 'Петров И.И.'б, 160),            # предмет, ФИО препода, часы лекций
#                ('начертался', 'Никифоров И.А.'б, 40),
#                ('3d-моделирование', 'Петров П.С.'б, 80)]
events = [IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError,
          '', '', '', '', '', '', '']

# TODO: нет. не имеет значения, т.к. choice берет рандомный вариант.
# Перемешал
random.shuffle(events)


def one_day():
    global events
    event = random.choice(events)
    # TODO: да, идею понимаю. Но наполнять events пустыми строка - не лучший вариант, потому что, что если вероятность
    #  исключения будет 6 к 100. Не будет же мы 94 пустых строки вписывать?
    #  Потому придумай альтернтивный вариант.
    if event:
        raise event
    else:
        return random.randint(1, 7)


ENLIGHTENMENT_CARMA_LEVEL = 777

# TODO: это константа?
CURRENT_CARMA_LVL = 0

while CURRENT_CARMA_LVL < ENLIGHTENMENT_CARMA_LEVEL:
    try:
        CURRENT_CARMA_LVL += one_day()
        print(CURRENT_CARMA_LVL)
    # TODO: перегрузи __str__ у классов исключений. А здесь сделай общий для всех обработчик.
    #  Перегрузил str? можешь вывести исключение принтом и получить нужное сообщение.
    except IamGodError:
        print('Так трудно быть богом')
    except DrunkError:
        print('Я не минздрав, но предупреждаю, что пить надо меньше')
    except CarCrashError:
        print('Страховая от тебя шифруется')
    except GluttonyError:
        print('На холодильник пора вешать замок')
    except DepressionError:
        print('Пора смотреть мелодраммы')
    except SuicideError:
        print('RIP')
