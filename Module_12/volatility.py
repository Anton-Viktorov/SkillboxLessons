import os
import csv
import operator


class TradesParser:

    def __init__(self, manager):
        self.manager = manager
        self.tikers = {}
        self.tikers_zero = []

    def run(self):
        for file in self.manager.get_file():
            with open(os.path.join('trades', file), newline='') as ff:
                reader = csv.reader(ff)
                next(reader)

                max_price = 0
                min_price = float("inf")

                for row in reader:
                    tiker, _, price, _ = row
                    max_price = max(max_price, float(price))
                    min_price = min(min_price, float(price))

                average_price = (max_price + min_price) / 2

                volatility = ((max_price - min_price) / average_price) * 100
                if volatility == 0:
                    self.tikers_zero.append(tiker)
                else:
                    self.tikers[tiker] = volatility


class ThreadManager:

    def __init__(self, threads_amt=1):
        self.path = 'trades'
        self.total_tikers = []
        self.total_tikers_zero = []
        self.threads_amt = threads_amt

    def get_file(self):
        for _, _, files in os.walk(self.path):
            for file in files:
                yield file

    def run(self):
        parsers = [TradesParser(manager=self) for _ in range(self.threads_amt)]
        for parser in parsers:
            parser.run()

        for parser in parsers:
            self.total_tikers += list(parser.tikers.items())
            self.total_tikers_zero += list(parser.tikers_zero)

    def sort_result(self):
        self.total_tikers.sort(key=operator.itemgetter(1), reverse=True)
        self.total_tikers_zero.sort()

    def print_result(self):
        self.sort_result()
        print('Максимальная волатильность:\n')

        for tiker, volatility in self.total_tikers[:3]:
            print(f"Tiker: {tiker} Volatility: {round(volatility, 1)}")

        print('Минимальная волатильность:\n')

        for tiker, volatility in self.total_tikers[-3:]:
            print(f"Tiker: {tiker} Volatility: {round(volatility, 1)}")

        print(f'Нулевая волатильность: {self.total_tikers_zero}')


if __name__ == '__main__':
    main_100500 = ThreadManager()
    main_100500.run()
    main_100500.print_result()

# TO DO: что за каша? почему ВСЕ внутри run. Менеджер потенциально может получить функции "добавить исполнителей"
#  или "убить исполнителя" или еще чего. А у нас в одном месте.

# TO DO: распаковку

# TO DO: распаковку

# TO DO: лучше использовать os.walk.
#  os.listdir - возвращает список. Т.е. он уже в памяти, поэтому итератор нам не сильно поможет.
#  Если в папке 1млн файлов, то они уже все в памяти.
#  А вот с помощью os.walk можно сделать генераторный метод, который будет возвращать по 1ому файлу.

# TO DO: используй itemgetter. Он в 1.5-2 раза быстрее, т.к. написан на Си

# TO DO: хорош)

# TO DO: max - хорош)

# TO DO: row[0], row[2] - это все не читабельно. Фиг пойми что там. Приходится лезть в файл и
#  смотреть, что возвращает строка. Распаковка эту проблему как раз решает и красиво решает.

# TO DO: можно сказать, что в main класс - Менеджер, который должен управлять парсингом и в будущем будет создавать
#  потоки. Упакую его в класс. Подсказка: записать все в run будет ошибкой. Менеджер будет один и у него должны
#  быть понятные методы.

# TO DO: не стоит писать класс так, чтобы он зависил от того, создаст ли кто-то снаружи то, что нам нужно.
#  Передай self менеджера в Исполнителя при создании, и там сохрани как manager.

# TO DO: все сломалось, потому что кто-то создал Менеджера, но не стал называть его так, как мы ожидали.
#  Но идея интересная. Первый кто так сделал.

# TO DO: еще можно было бы через next достать первую строку и иницировать max_price, min_price
#  первым значением. Но так тоже хорошо. Исправлять не обязательно.

# TO DO: сделай распаковку row (новички не пользуются распаковкой, а ты пользуйся, это выделит тебя
#  из толпы).

# TO DO: И какая же волталиность у этго Тикера? я угадаю! ноль?
#  Как угадал? не спрашивай, это магия Новатского.
#  Зачем нам тогда словарь?

# TO DO: сепараторы лучше не задавать. os.path.join.
#  в windows и Linux разные сепараторы, а питон кроссплатформенный.

# TO DO: не надо округлять ВНУТРИ программы. Округление ВСЕГДА на выходе.
#  Нам людям удобно смотреть на округленные числа, а программе удобнее на длинные.
