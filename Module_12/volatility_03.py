import os
import operator
from multiprocessing import Process, Queue
from queue import Empty
import math
import csv


class TradesParser(Process):
    def __init__(self, queue, file_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tickers = {}
        self.tickers_zero = []
        self.result_queue = queue
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

                self.result_queue.put((ticker, volatility))


class ProcessManager:

    def __init__(self, process_amt=4):
        self.path = 'trades'
        self.file_list = os.listdir(self.path)
        self.total_tickers = []
        self.total_tickers_zero = []
        self.process_amt = process_amt
        self.result_queue = Queue(maxsize=self.process_amt * 4)

        self.files_amt = math.ceil(len(self.file_list) / self.process_amt)

    def run(self):
        parsers = []
        for i in range(self.process_amt):
            files = self.file_list[i * self.files_amt:self.files_amt * (i+1)]
            parser = TradesParser(file_list=files, queue=self.result_queue)
            parsers.append(parser)

        for parser in parsers:
            parser.start()

        while True:
            try:
                ticker, volatility = self.result_queue.get(timeout=0.5)
                if volatility == 0:
                    self.total_tickers_zero.append(ticker)
                else:
                    self.total_tickers.append((ticker, volatility))
            except Empty:
                if not any(parser.is_alive() for parser in parsers):
                    break

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
    main_100500 = ProcessManager()
    main_100500.run()
    main_100500.print_result()


# TO DO: упростить строку

# TO DO: ну 5 секунд много. 0.5 более чем достаточно. Ведь если еще кто-то жив и
# ему попался жирный файл,
#  то цикл все равно не прервется.

# TO DO: раздели и округли в большую сторону ...

# TO DO: Завяжи размер на число исполнителей. вдруг их будет 32? (на сервере вполне может быть и 100)

# TO DO: запятая не обязательна на конце, если в кортеже 2+ элемента
#  Её ставят, если нужен кортеж из 1го элемента: (x,) и (x,y).
#  Во втором месте тоже поправь.

# TO DO:
#  внутри списокового включения не стоит выполнять print`ов, append`ов.
#  pop - Тоже на грани. Так обычно не пишут.
#  .
#  переменная parser, из цикла выше, это индекс парсера.
#  Используй этот индекс, чтобы взять нужны срез из self.file_list.
#  .
#  Кстати, индекс лучше назвать иначе. Даже i будет лучше.

# TO DO: сначала импорт внутренних, потом скачанных, потом своих.
#  csv - сторонний, не внутренний. Его импортируем в конце, после встроенных модулей.

# TO DO: неее. а вдруг файлов 100500?
# TO DO: сейчас можно сказать, у нас выполнена упрощенная версия. Почему?
# Потому что мы создаем канал бесконечного
#  размера. Представим, что обработка файла занимает 4 минуты 1 процессом-парсером,
#  и 1 минуту процессом-управляющим.
#  Тогда мы создадим 4 процесса-парсера и в среднем они будут парсить 4 файла за
#  4 минуты (при условии что у нас
#  хотя бы 4 ядра) + 1 процесс-управляющий.
#  Представим, что файлов 1000 шт.
#  .
#  Как сейчас будет работать код?
#  1000 минут будет парсить, напихает в канал 100500 элементов, потом завершаться
#  все процессы-парсеры и включиться
#  процесс-управляющий. В этот момент файл пайпа может занимать гигабайты памяти.
#  .
#  Как бы мы хотели, чтобы работало?
#  Потоки-парсеры парсят данные и добавляют в ОЧЕРЕДЬ (не 4 пайпа, а одна очередь). Размер очереди, допустим х4
#  от числа процессов, т.е. 16.
#  Парсеры парсят, а процесс-управляющий, берет готовые данные, сразу как-только что-то появилось и тоже
#  подключается в работу.
#  .
#  Какой профит?
#  1. Размер очереди жестко ограничен, и мы уверены, что не будет такого числа файлов,
#  чтобы у нас не хватило ОЗУ;
#  2. Не 4, а 5 процессов выполняются параллельно. Поэтому работа будет закончена ~ в 2 раза
#  быстрее (примечение:
#     в 2 раза в условия описанной задачи в первых 2х предложения);
