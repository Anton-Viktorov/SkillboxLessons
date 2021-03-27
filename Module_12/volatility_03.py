import os
import csv
import operator
from multiprocessing import Pipe, Process


class TradesParser(Process):
    def __init__(self, pipe, file_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tickers = {}
        self.tickers_zero = []
        self.pipe = pipe
        self.files_list = file_list

    def run(self):
        for file in self.files_list:
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

        self.pipe.send([list(self.tickers.items()), self.tickers_zero])
        self.pipe.close()


class ThreadManager:

    def __init__(self, process_amt=4):
        self.path = 'trades'
        self.file_list = os.listdir(self.path)
        self.total_tickers = []
        self.total_tickers_zero = []
        self.process_amt = process_amt
        self.files_amt = len(self.file_list) // self.process_amt

    # def get_file(self):
    #     for file in self.file_list:
    #         self.file_queue.put(file)

    def run(self):
        parsers = []
        pipes = []
        for parser in range(self.process_amt - 1):
            manager_pipe, parser_pipe = Pipe()
            files = [self.file_list.pop() for _ in range(self.files_amt)]
            parser = TradesParser(pipe=parser_pipe, file_list=files)
            parsers.append(parser)
            pipes.append(manager_pipe)

        manager_pipe, parser_pipe = Pipe()
        parser = TradesParser(pipe=parser_pipe, file_list=self.file_list)
        parsers.append(parser)
        pipes.append(manager_pipe)

        for parser in parsers:
            parser.start()

        for parser in parsers:
            parser.join()

        for pipe in pipes:
            tickers, tickers_zero = pipe.recv()
            self.total_tickers += tickers
            self.total_tickers_zero += tickers_zero

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

        print(len(self.total_tickers) + len(self.total_tickers_zero))


if __name__ == '__main__':
    main_100500 = ThreadManager()
    main_100500.run()
    main_100500.print_result()
