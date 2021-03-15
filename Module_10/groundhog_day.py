# -*- coding: utf-8 -*-
import random


# Сначала я вообще не понял задание. Думал, что исключение должно выпадать каждый день.
# Акаждому исключению нужно присвоить некий "вес вероятности".
# Даже нашел алгоритм с random.choice(), который учитывает эту вероятность. Но потом походил подумал,
# что что-то не сходится. А потом дошло, что исключение может и не выпасть. И дело пошло)

class IamGodError(Exception):

    def __str__(self):
        return f'Так трудно быть богом'


class DrunkError(Exception):

    def __str__(self):
        return f'Я не минздрав, но предупреждаю, что пить надо меньше'


class CarCrashError(Exception):

    def __str__(self):
        return f'Страховая от тебя шифруется'


class GluttonyError(Exception):

    def __str__(self):
        return f'На холодильник пора вешать замок'


class DepressionError(Exception):

    def __str__(self):
        return f'Пора смотреть мелодраммы'


class SuicideError(Exception):

    def __str__(self):
        return f'RIP'


events = (IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError,)


def one_day():

    if random.randint(1, 13) == 1:
        raise random.choice(events)
    else:
        return random.randint(1, 7)

    # one_more_day = random.choices(['exception', 'regular day'], weights=[0.08, 0.92])
    #
    # if 'exception' == one_more_day:
    #     raise random.choice(events)
    # else:
    #     return random.randint(1, 7)


ENLIGHTENMENT_CARMA_LEVEL = 777
current_carma_lvl = 0

while current_carma_lvl < ENLIGHTENMENT_CARMA_LEVEL:
    try:
        current_carma_lvl += one_day()
        print(current_carma_lvl)
    except events as e:
        print(e)

# TO DO: если объект не присваивается, а только читается, не обязательно global писать.
#  По крайней мере с точки зрения синтаксиса. По стилю тут не могу точно сказать, не оговорено.

# TO DO: тут мы действуем по причипу "проще просить прощения, чем испрашивать разрешения".
#  Это чисто python принцип. Но я придерживаюсь: не нужно везде перехватывать исключения, чтобы что-то проверить.
#  Как бы ты сделал без исключения?
#  Помимо этого, задание говорит: что с вероятностью 1 к 13 может быть исключение. А сейчас вероятность 6 к 13.

# Список возможных исключений
# TO DO:
#  1. пусть будут только исключени;
#  2. лучше кортеж использовать, если список не собираемся модицифировать.
#       Кортежи полезны в 2х случаях:
#           1. список-константа;
#           2. для хранения полей одной сущности. Например: список предметов в универе:
#               [('матан', 'Петров И.И.'б, 160),            # предмет, ФИО препода, часы лекций
#                ('начертался', 'Никифоров И.А.'б, 40),
#                ('3d-моделирование', 'Петров П.С.'б, 80)]

# TO DO: это константа?

# TO DO: перегрузи __str__ у классов исключений. А здесь сделай общий для всех обработчик.
#  Перегрузил str? можешь вывести исключение принтом и получить нужное сообщение.

# TO DO: да, идею понимаю. Но наполнять events пустыми строка - не лучший вариант, потому что, что если вероятность
#  исключения будет 6 к 100. Не будет же мы 94 пустых строки вписывать?
#  Потому придумай альтернтивный вариант.

# TO DO: нет. не имеет значения, т.к. choice берет рандомный вариант.
