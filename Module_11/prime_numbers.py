# -*- coding: utf-8 -*-
# Есть функция генерации списка простых чисел

# def get_prime_numbers(n):
#     prime_numbers = []
#     for number in range(2, n+1):
#         for prime in prime_numbers:
#             if number % prime == 0:
#                 break
#         else:
#             prime_numbers.append(number)
#     return prime_numbers


# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:

    def __init__(self, n):
        self.n = n
        # TO DO: не. Мы сейчас храним все числа.
        #  Да, это выгодно: посчитал 1 раз и дальше используешь.
        #  Но итераторы решают другуюп проблему, должны решать: если чисел 100500 штук. И они просто не влезают
        #  в память компа. А еще пользователь может взять только первые 10 чисел и успокоиться, а мы все N чисел
        #  посчитали.
        #  .
        #  Сделай так, чтобы числа не хранились.
        self.iter = 1

    # TO DO: функция ответчае "да" или "нет".
    #  На какой вопрос?
    #  Как лучше тогда назвать метод?  (для примера повспоминай какие встроенные функции встречались, которые тоже
    #                                   отвечаи "да" или "нет")
    def is_iter(self):
        # TO DO: раз модуль math импортируем, используй ceil
        # Я передумал) Забыл удалить.
        for x in range(2, int(self.iter ** 0.5) + 1):
            if self.iter % x == 0:
                return False
        return True

    def __iter__(self):
        self.iter = 1
        return self

    def __next__(self):
        self.iter += 1
        if self.iter >= self.n:
            raise StopIteration
        elif self.is_iter():
            return self.iter
        else:
            # TO DO: лучше next(self). метод __ххххх__ не принято так вызывать.
            #  Единственное исключение: super().__init__.
            return next(self)


# TO DO: опять заменил, т.к. так легче увидеть не пропущены ли числа.
# prime_number_iterator = PrimeNumbers(n=100)
# for number in prime_number_iterator:
#     print(number, end=', ')

# Сделал обе сразу

# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик

# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.


def primes_number_generator(n, number_type):
    for prime in range(2, n+1):
        for x in range(2, int(prime ** 0.5) + 1):
            if prime % x == 0:
                break
        else:
            if number_type(prime):
                yield prime


def is_happy(number):
    number_str = str(number)
    length = len(number_str)

    part_1 = [int(x) for x in number_str[:int(length // 2)]]

    if length % 2 == 0:
        part_2 = [int(x) for x in number_str[int(length // 2):]]
    else:
        part_2 = [int(x) for x in number_str[int(length // 2) + 1:]]

    return sum(part_1) == sum(part_2)


def is_palindrome(number):
    number_str = str(number)
    length = len(number_str)

    part_1 = [int(x) for x in number_str[:int(length // 2)]]

    if length % 2 == 0:
        part_2 = [int(x) for x in number_str[int(length // 2):]]
    else:
        part_2 = [int(x) for x in number_str[int(length // 2) + 1:]]

    return part_1 == part_2[::-1]


happy_primes_100 = primes_number_generator(n=100, number_type=is_happy)
for prime in happy_primes_100:
    print(prime, end=', ')
