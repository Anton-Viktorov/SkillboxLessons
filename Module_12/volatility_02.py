import os
import csv
import operator
import threading
from threading import Thread


class TradesParser(Thread):

    def __init__(self, manager, generator, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.tickers = {}
        self.tickers_zero = []
        self.generator = generator
        self.generator_lock = lock

    def run(self):
        while True:
            try:
                with self.generator_lock:
                    self.manager.generator_calls += 1
                    file = next(self.generator)
            except StopIteration:
                break

            # TODO: else тут лишний. Он сдвинул весь код правее. Чем больше вложенность, тем хуже читабельность.
            #  В except стоит break.
            else:
                with open(os.path.join('trades', file), newline='') as ff:
                    reader = csv.reader(ff)
                    next(reader)

                    max_price = 0
                    min_price = float("inf")

                    for row in reader:
                        ticker, _, price, _ = row
                        max_price = max(max_price, float(price))
                        min_price = min(min_price, float(price))

                    average_price = (max_price + min_price) / 2

                    volatility = ((max_price - min_price) / average_price) * 100
                    if volatility == 0:
                        self.tickers_zero.append(ticker)
                    else:
                        self.tickers[ticker] = volatility


class ThreadManager:

    def __init__(self, threads_amt=4):
        self.path = 'trades'
        self.total_tickers = []
        self.total_tickers_zero = []
        self.threads_amt = threads_amt
        self.lock = threading.Lock()
        self.file_generator = self.get_file()
        self.generator_calls = 0

    def get_file(self):
        for *_, files in os.walk(self.path):
            for file in files:
                yield file

    def run(self):
        parsers = [TradesParser(manager=self, generator=self.file_generator, lock=self.lock)
                   for _ in range(self.threads_amt)]
        for parser in parsers:
            parser.start()

        for parser in parsers:
            parser.join()

        for parser in parsers:
            self.total_tickers += list(parser.tickers.items())
            self.total_tickers_zero += list(parser.tickers_zero)

    def sort_result(self):
        self.total_tickers.sort(key=operator.itemgetter(1), reverse=True)
        self.total_tickers_zero.sort()

    def print_result(self):
        self.sort_result()

        print('Максимальная волатильность:')
        for ticker, volatility in self.total_tickers[:3]:
            print(f"Ticker: {ticker} Volatility: {round(volatility, 1)}")

        print('\nМинимальная волатильность:')
        for ticker, volatility in self.total_tickers[-3:]:
            print(f"Ticker: {ticker} Volatility: {round(volatility, 1)}")

        print(f'\nНулевая волатильность: {self.total_tickers_zero}')

        print(f'\nВсего обращений к генератору: {self.generator_calls}. Файлов: 112')


if __name__ == '__main__':
    main_100500 = ThreadManager()
    main_100500.run()
    main_100500.print_result()
