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
events = [IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError,
          '', '', '', '', '', '', '']
# Перемешал
random.shuffle(events)


def one_day():
    global events
    event = random.choice(events)
    if event:
        raise event
    else:
        return random.randint(1, 7)


ENLIGHTENMENT_CARMA_LEVEL = 777
CURRENT_CARMA_LVL = 0

while CURRENT_CARMA_LVL < ENLIGHTENMENT_CARMA_LEVEL:
    try:
        CURRENT_CARMA_LVL += one_day()
        print(CURRENT_CARMA_LVL)
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
