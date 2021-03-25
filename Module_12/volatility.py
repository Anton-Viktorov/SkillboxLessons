import os
import csv
from collections import defaultdict


class TradesParser:

    def __init__(self):
        self.tikers = defaultdict(int)
        self.tikers_zero = defaultdict(int)

    def run(self):
        try:
            file = main.get_file()
            with open(f"trades/{file}", newline='') as ff:
                reader = csv.reader(ff)
                next(reader)

                max_price = 0
                min_price = float("inf")

                for row in reader:
                    tiker = row[0]
                    price = float(row[2])
                    max_price = max(max_price, price)
                    min_price = min(min_price, price)

                average_price = (max_price + min_price) / 2
                volatility = round(((max_price - min_price) / average_price) * 100, 1)
                if volatility == 0:
                    self.tikers_zero[tiker] = volatility
                else:
                    self.tikers[tiker] = volatility
        except StopIteration:
            pass
        else:
            self.run()


class ThreadManager:

    def __init__(self, threads_amt=4):
        self.path = 'trades/'
        self.total_tikers = []
        self.total_tikers_zero = []
        self.file_list = iter(os.listdir(self.path))
        self.threads_amt = threads_amt

    def get_file(self):
        return next(self.file_list)

    def run(self):
        parsers = [TradesParser() for _ in range(self.threads_amt)]
        for parser in parsers:
            parser.run()

        for parser in parsers:
            self.total_tikers += list(parser.tikers.items())
            self.total_tikers_zero += list(parser.tikers_zero.keys())

        self.total_tikers.sort(key=lambda i: i[1], reverse=True)
        self.total_tikers_zero.sort()

        print('Максимальная волатильность:\n')
        for tiker in self.total_tikers[:3]:
            print(f"Tiker: {tiker[0]} Volatility: {tiker[1]}")

        print('Минимальная волатильность:\n')
        for tiker in self.total_tikers[-3:]:
            print(f"Tiker: {tiker[0]} Volatility: {tiker[1]}")

        print(f'Нулевая волатильность: {self.total_tikers_zero}')


# TO DO: можно сказать, что в main класс - Менеджер, который должен управлять парсингом и в будущем будет создавать
#  потоки. Упакую его в класс. Подсказка: записать все в run будет ошибкой. Менеджер будет один и у него должны
#  быть понятные методы.


if __name__ == '__main__':
    main = ThreadManager()
    main.run()
