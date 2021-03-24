import os
import csv
from collections import defaultdict


class TradesParser:

    def __init__(self, file_name):
        self.path = f'trades/{file_name}'
        self.tikers = defaultdict(int)
        self.tikers_zero = defaultdict(int)

    def run(self):
        with open(f"{self.path}", newline='') as ff:
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


def main():
    tikers = []
    tikers_zero = []
    file_list = os.listdir(path='trades/')
    parsers = [TradesParser(file_name=file) for file in file_list]
    for parser in parsers:
        parser.run()

    for parser in parsers:
        tikers += list(parser.tikers.items())
        tikers_zero += list(parser.tikers_zero.keys())

    tikers.sort(key=lambda i: i[1], reverse=True)
    tikers_zero.sort()

    print('Максимальная волатильность:\n')
    for tiker in tikers[:3]:
        print(f"Tiker: {tiker[0]} Volatility: {tiker[1]}")

    print('Минимальная волатильность:\n')
    for tiker in tikers[-3:]:
        print(f"Tiker: {tiker[0]} Volatility: {tiker[1]}")

    print(f'Нулевая волатильность: {tikers_zero}')


if __name__ == '__main__':
    main()
