import os
import csv
from collections import defaultdict


class TradesParser:

    def __init__(self):
        self.tikers = defaultdict(int)
        self.tikers_zero = defaultdict(int)

    def run(self):
        try:
            # TODO: все сломалось, потому что кто-то создал Менеджера, но не стал называть его так, как мы ожидали.
            #  Но идея интересная. Первый кто так сделал.
            file = main.get_file()
            with open(f"trades/{file}", newline='') as ff:
                reader = csv.reader(ff)
                next(reader)

                max_price = 0
                min_price = float("inf")        # TODO: хорош)

                # TODO: еще можно было бы через next достать первую строку и иницировать max_price, min_price
                #  первым значением. Но так тоже хорошо. Исправлять не обязательно.


                # TODO: сделай распаковку row (новички не пользуются распаковкой, а ты пользуйся, это выделит тебя
                #  из толпы).
                for row in reader:
                    # TODO: row[0], row[2] - это все не читабельно. Фиг пойми что там. Приходится лезть в файл и
                    #  смотреть, что возвращает строка. Распаковка эту проблему как раз решает и красиво решает.
                    tiker = row[0]
                    price = float(row[2])
                    max_price = max(max_price, price)       # TODO: max - хорош)
                    min_price = min(min_price, price)

                average_price = (max_price + min_price) / 2

                # TODO: не надо округлять ВНУТРИ программы. Округление ВСЕГДА на выходе.
                #  Нам людям удобно смотреть на округленные числа, а программе удобнее на длинные.
                volatility = round(((max_price - min_price) / average_price) * 100, 1)
                if volatility == 0:
                    # TODO: И какая же волталиность у этго Тикера? я угадаю! ноль?
                    #  Как угадал? не спрашивай, это магия Новатского.
                    #  Зачем нам тогда словарь?
                    self.tikers_zero[tiker] = volatility
                else:
                    self.tikers[tiker] = volatility
        except StopIteration:
            pass
        else:
            # TODO: если будет 1млн файлов, то у нас стэка не хватит, хранить столько вложенных run`ов
            self.run()


class ThreadManager:

    def __init__(self, threads_amt=4):
        # TODO: сепараторы лучше не задавать. os.path.join.
        #  в windows и Linux разные сепараторы, а питон кроссплатформенный.
        self.path = 'trades/'
        self.total_tikers = []
        self.total_tikers_zero = []
        self.file_list = iter(os.listdir(self.path))
        self.threads_amt = threads_amt

    def get_file(self):
        # TODO: лучше использовать os.walk.
        #  os.listdir - возвращает список. Т.е. он уже в памяти, поэтому итератор нам не сильно поможет.
        #  Если в папке 1млн файлов, то они уже все в памяти.
        #  А вот с помощью os.walk можно сделать генераторный метод, который будет возвращать по 1ому файлу.
        return next(self.file_list)

    def run(self):
        parsers = [TradesParser() for _ in range(self.threads_amt)]
        for parser in parsers:
            parser.run()

        for parser in parsers:
            self.total_tikers += list(parser.tikers.items())
            self.total_tikers_zero += list(parser.tikers_zero.keys())

        # TODO: используй itemgetter. Он в 1.5-2 раза быстрее, т.к. написан на Си
        self.total_tikers.sort(key=lambda i: i[1], reverse=True)
        self.total_tikers_zero.sort()

        print('Максимальная волатильность:\n')
        # TODO: распаковку
        for tiker in self.total_tikers[:3]:
            print(f"Tiker: {tiker[0]} Volatility: {tiker[1]}")

        print('Минимальная волатильность:\n')
        # TODO: распаковку
        for tiker in self.total_tikers[-3:]:
            print(f"Tiker: {tiker[0]} Volatility: {tiker[1]}")

        print(f'Нулевая волатильность: {self.total_tikers_zero}')

        # TODO: что за каша? почему ВСЕ внутри run. Менеджер потенциально может получить функции "добавить исполнителей"
        #  или "убить исполнителя" или еще чего. А у нас в одном месте.


# TO DO: можно сказать, что в main класс - Менеджер, который должен управлять парсингом и в будущем будет создавать
#  потоки. Упакую его в класс. Подсказка: записать все в run будет ошибкой. Менеджер будет один и у него должны
#  быть понятные методы.


if __name__ == '__main__':
    # TODO: не стоит писать класс так, чтобы он зависил от того, создаст ли кто-то снаружи то, что нам нужно.
    #  Передай self менеджера в Исполнителя при создании, и там сохрани как manager.
    main_100500 = ThreadManager()
    main_100500.run()
