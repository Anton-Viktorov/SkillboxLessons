from termcolor import cprint

# Test commit # another commit from github


class House:
    """Создаем объект: дом"""

    def __init__(self):
        self.money = 100
        self.fridge = 50
        self.dust_amt = 0
        self.total_bank = 0  # Общий банк. Сколько всего муж заработает за год.

    def __str__(self):
        return f"House: \n Money in box: {self.money}, " \
               f"food in fridge: {self.fridge}, " \
               f"dust amount: {self.dust_amt}"

    def dust_append(self):
        self.dust_amt += 5  # Уровень грязи в доме


class Being:
    """Класс-родитель. Инициализирует модель чего-то живого(человека, кота и т.д.)"""

    def __init__(self, name, home, fullness=30):
        self.name = name
        self.fullness = fullness
        self.home = home

    def __str__(self):
        return f"Name: {self.name}, fullness: {self.fullness}"  # Выводим общую информацию об объекте

    def eat(self):
        portion = min(30, self.home.fridge)
        self.fullness += portion
        self.home.fridge -= portion
        print(f"{self.name} eating. Fullness + {portion}")

    def is_alive(self):
        # TODO: еще одна хитрость.
        #  "self.fullness > 0" сам по себе дает True|False. Нам не нужен if|else, можно сравнение
        #  подставить сразу в return
        if self.fullness > 0:
            return True
        else:
            return False


class Husband(Being):
    """Создаем объект: муж"""

    def __init__(self, name, home):
        super().__init__(name=name, home=home)
        self.happiness_level = 100

    def __str__(self):
        return f"Муж. {super().__str__()}, happiness level: {self.happiness_level}"

    def is_alive(self):
        # TODO: упростить. if должен ичезнуть.
        #  Использование super().is_alive() - хорошо!
        if super().is_alive() and self.happiness_level > 10:
            return True
        else:
            return False

        # TODO: еще одна фишка:
        #  and как и or очень сильно оптимизированы. Если and видит, что первый операнд дает False, то он не будет
        #  проверять правый операнд. Пример:
        #       False and 1 / 0
        #       None and 1 / 0      # ошибки нет
        #  .
        #  Для or такая же тема, но используется в другом контексте:
        #       True or 1 / 0       # если слева Тру, он не будет смотреть правую часть
        #  .
        #  Но можно так:
        #       x = val_1 or val_2  # если val_1 будет ~True, То в x сохранится val_1.
        #                           # если val_1 будет похож на False, то сохранится val_2
        x = 100500 or 123       # 100500
        y = None or 123         # 123
        # TODO: проверь в интепрераторе вручную, чтобы запомнить.

    def act(self):
        if self.home.dust_amt >= 90:
            self.happiness_level -= 10  # Проверяем насколько грязно дома

        if self.fullness <= 10:
            self.eat()
            return

        if self.happiness_level <= 20:
            self.gaming()
            return

        self.work()

        # TODO: проще все объединить через if/elif/else, чтобы не писать return внутри каждого if`а.

    def work(self):
        self.fullness -= 10
        self.home.money += 150
        self.home.total_bank += 150  # Добавляем информацию о суммарном заработке за год
        print(f"{self.name} working. Money in box + 150 ")

    def gaming(self):
        self.fullness -= 10
        self.happiness_level += 20
        print(f"{self.name} playing WOT. Happiness + 20 ")


class Wife(Being):
    """Создаем объект: жена"""

    def __init__(self, name, home):
        super().__init__(name=name, home=home)
        self.happiness_level = 100
        self.fur_coat_collection = 0  # Коллекция шуб жены. Для подсчета суммы купленных шуб.

    def __str__(self):
        return f"Жена. {super().__str__()}, happiness level: {self.happiness_level}"

    def is_alive(self):
        if super().is_alive() and self.happiness_level > 10:
            return True
        else:
            return False

    def act(self):
        if self.home.dust_amt >= 90:
            self.happiness_level -= 10  # Проверяем насколько грязно дома

        if self.fullness <= 20:
            self.eat()
            return

        if self.happiness_level <= 20 and self.home.money > 350:  # Хватит ли денег на шубу
            self.buy_fur_coat()
            return

        self.clean_house()

    def shopping(self):
        self.fullness -= 10
        food_pay = min(60, self.home.money)
        self.home.fridge += food_pay
        self.home.money -= food_pay
        print(f"{self.name} shopping. Food in fridge + {food_pay}")

    def buy_fur_coat(self):
        self.fullness -= 10
        self.happiness_level += 60
        self.home.money -= 350
        self.fur_coat_collection += 1
        print(f"{self.name} buys fur coat. Happiness + 60")

    def clean_house(self):
        self.fullness -= 10
        self.home.dust_amt -= min(self.home.dust_amt, 100)
        print(f"{self.name} washes house")


home1 = House()
serge = Husband(name='Сережа', home=home1)
masha = Wife(name='Маша', home=home1)

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    home1.dust_append()
    if serge.is_alive():
        serge.act()
    else:
        cprint(f"{serge.name} умер. Помним, любим, скорбим...", color='red')

    if masha.is_alive():
        masha.act()
    else:
        cprint(f"{masha.name} умерла. Помним, любим, скорбим...", color='red')

    # Я не уверен в if-ах которые написал выше. В том, что они грамотно подходят. Поэтому думал сделать такую штуку.
    # Однако в этой ситуации будет проблематично понять, кто именно умер.
    # if serge.is_alive() and masha.is_alive():
    #     serge.act()
    #     masha.act()
    # else:
    #     print(f"Один из членов семьи умер.")

    # TODO: согласен. Стремнова-то. Вариант выше выглядит симпатично. Можешь его сделать основным.
    #  Но в дальнейшем мы сделаем другой вариант.

    cprint(serge, color='cyan')
    cprint(masha, color='cyan')

cprint(f"{serge.name} заработал {home1.total_bank} за год", color='red')
cprint(f"{masha.name} купила {masha.fur_coat_collection} шуб за год", color='red')

# TO DO: пусть если грази меньше чем 100, но она есть, мы будем убирать сколько есть.
#  .
#  Выгодно будет использовать такой фокус:
#   cur_lvl = min(30, текущий_уровень_грязи)
#  .
#  И потом мы убираем cur_lvl единиц грязи в доме (либо 100, если ее много, либо всю, если ее меньше 100).

# TO DO: посмотри на if|else ниже. Все отличие только в том 60 или ВСЕ ДЕНЬГИ. Упрости, чтобы одинаковый код
#  был вынесен ДО или ПОСЛЕ if/else.

# TO DO: тут стоит без result обойтись. Как и в случае с мужем. Т.к. действие "super().__str__()" очевидно,
#  это не усложнит код. Тонкая грань. Это не ошибка, но скажем, warning по стилю кода.

# TO DO: жена тоже ест. У нее этот же метод один в один (почти)
#  Почти наверняка ты скопировал класс Муж и на его основа сделал Жену, прям костплеешь Бога, он Адама за основу
#  брал.

# TO DO: эту проверку нам удобнее реализовать в отдельном методе is_alive. Который будет возвращать True\False.
#  У котов счастья нет - они могут умирать только от голода. А люди и от голода, и от несчастий.
#  Подумай насчет этого метода и реализуй его обязательно.

# TO DO: ну "роль" это так себе поле. Обычно поле объекта как-то описывает именно его сущность.
#  Например "имя". У разных объектов Мужей будут разные имена. А тут у всех будет одна роль "муж".
#  .
#  Если появляется необходиомть сделать 1 поле для ВСЕХ объектов - используй поле класса.
#  .
#  По данному полю, рекомендую его убрать, т.к. он используется только в __str__, а тут жестко записать "Муж". done

# TO DO: это поле класса. Чем оно отличается от поля объекта?

# TO DO: у кота нет уровня счастья. Нет для него такого понятия. done

# TO DO: красава, что додумался.

# TO DO: небольшная справка, не обязательная к исполнению: довольно часто amount, counter сокращают в amt, cnt

# TO DO: лучше не давать длинных имен. В частности ОЧЕНЬ редко используют "_in_" или "_а_" в названии.
#  Как одним словом сократить?

# TO DO: молодец, что длина строки ни разу не пересекла 120 символов.

# TO DO: лучше избегать вложенности if`ов если это возможно. Пример:
#          def do_something(x, y):
#               if x:
#                   if y:
#                       print('done!')
#                   else:
#                       print('failed in Y')
#               else:
#                   print('failed in X')
#  .
#  Громоздко, не правда ли? Мы может упростить эту же функцию:
#           def do_something(x, y):
#               if not x:
#                   print('failed in X')
#                   return
#               if not y:
#                   print('failed in Y')
#                   return
#               print('done!')
#  .
#  А? Сразу исчезает два уровня вложенности, у каждого условия возможен выход по ошибке. Куда легче ориентироваться,
#  внутри функции) В цикле вместо return будет стоять continue (переход к следующей итерацие).


# TO DO: проблема, которую упустил в прошлый раз (про переменную home внутри классов)
#  Переименовал переменную и все классы выше померли. Они работают, только с одной переменной - home.
#  А если нужно создать 2 семьи, которые живу в разных домах?
#  Или например семья переедет в новый дом. Допустим в версии 100500 такое появится, заказчик попросит добавить.