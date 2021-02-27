from termcolor import cprint


class House:
    """Создаем объект: дом"""

    def __init__(self):
        self.money = 100
        # TO DO: food тоже как вариант, но я за fridge)
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
        # TO DO: используй фокус с min, который для грязи применяли
        portion = min(30, self.home.fridge)
        self.fullness += portion
        self.home.fridge -= portion
        print(f"{self.name} eating. Fullness + {portion}")

    # TO DO: т.к. мы планируем этот класс сделать общим для людей и котов. Пусть в нем не будет счастья совсем.
    #  КОгда мы будем создавать класс Муж/Жена, то мы перегрузим ему метод is_alive и через super().is_alive() вызовем
    #  родительский is_alive. Если не знаком с super() - это обращение к родительскому методу. Пример:
    #   class A:
    #       def fun():
    #           print('весело!')
    #   .
    #   class B(A):     # наследуется от А
    #       def fun():
    #           super().fun()       # вызываем метод fun у нашего родителя
    #           print('весело №2!')
    #   .
    #   is_alive надо организовать по подобной схеме. Муж/Жена будут перегружать is_alive и дополнять его.
    #   Т.е. прямо говоря: текущий is_alive проверяет только сытость. А те у кого есть счастье дополнят его.
    def is_alive(self):
        if self.fullness > 0:
            return True
        else:
            return False

        # TO DO: Это образцово плохая вложенность (см чуть ниже)


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


class Husband(Being):
    """Создаем объект: муж"""

    X = 100500  # TO DO: это поле класса. Чем оно отличается от поля объекта?

    # Атрибуты в поле класса относятся к самому классу. К ним можно обратиться не создавая объект.
    # Атрибуты в поле объекта являются атрибутами объекта. Для работы с ними нужно инициализировать объект.
    # При этом обратиться и использовать атрибут класса можно через экземпляр. Т.е. атрибут класса будет
    # атрибутом конкретного объекта класса. До тех пор пока мы не переопределим значение этого атрибута.
    # При переопределении значения, атрибут объекта будет ссылаться на новое значение, а старая связь будет утрачена.

    # TO DO: важный аспект, который не прозвучал: аттрибут класса - один на все объекты.
    #  Т.е. Х выше будет один на всех. И если его поменять: "Husband.X = 123", то он изменится у всех объектов-мужей.

    # Про это не упомянул, да. Может, на тот момент, показалось очевидным фактом. Т.к. я сказал, что атрибут класса
    # является атрибутом для экземпляра.

    def __init__(self, name, home):
        super().__init__(name=name, home=home)
        self.happiness_level = 100

    def __str__(self):
        # TO DO: харош # Спасибо
        return f"Муж. {super().__str__()}, happiness level: {self.happiness_level}"

    def is_alive(self):
        if super().is_alive() and self.happiness_level > 10:
            return True
        else:
            return False

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

        # TO DO: вообще is_alive мы уберем от сюда, будем проверять "Жив или нет" в цикле симуляции.
        #  Иначе метод будет 2 раза вызываться.

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
        # TO DO: как можно упростить?
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
        # TO DO: переменная cur_lvl используется 1 раз. Поэтому можно ее не создавать..
        self.home.dust_amt -= min(self.home.dust_amt, 100)
        print(f"{self.name} washes house")


# TO DO: проблема, которую упустил в прошлый раз.
#  Переименовал переменную и все классы выше померли. Они работают, только с одной переменной - home.
#  А если нужно создать 2 семьи, которые живу в разных домах?
#  Или например семья переедет в новый дом. Допустим в версии 100500 такое появится, заказчик попросит добавить.
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
