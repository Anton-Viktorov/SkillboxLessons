# -*- coding: utf-8 -*-

# Умножить константу BRUCE_WILLIS на пятый элемент строки, введенный пользователем

try:
    BRUCE_WILLIS = 42

    input_data = input('Если хочешь что-нибудь сделать, сделай это сам: ')
    leeloo = int(input_data[4])
    result = BRUCE_WILLIS * leeloo
    print(f"- Leeloo Dallas! Multi-pass № {result}!")
except ValueError as e:
    print(f"Ошибка преобразования в целое число. {e.args}")
except IndexError as e:
    print(f"Входной список слишком короткий. Нет элемента с индексом 4")
except Exception as e:
    print(f"Непредвиденная ошибка. Информация: {e}")

# TODO: ok
