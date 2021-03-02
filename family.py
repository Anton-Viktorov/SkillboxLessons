from termcolor import cprint
import random


class House:
    """Создаем объект: дом"""

    cat_food = 30

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
        return self.fullness > 0


class Husband(Being):
    """Создаем объект: муж"""

    def __init__(self, name, home):
        super().__init__(name=name, home=home)
        # TODO: такое же поле у Жены
        self.happiness_level = 100

    def __str__(self):
        return f"Муж. {super().__str__()}, happiness level: {self.happiness_level}"

    # TODO: такой же метод у Жены
    def is_alive(self):
        return super().is_alive() and self.happiness_level > 10

    def act(self):
        if self.home.dust_amt >= 90:
            self.happiness_level -= 10  # Проверяем насколько грязно дома

        if self.fullness <= 20:
            self.eat()
        elif self.happiness_level <= 20:
            self.gaming()
        elif self.happiness_level <= 30:
            self.pet_the_cat()
        else:
            self.work()

    def work(self):
        self.fullness -= 10
        self.home.money += 150
        self.home.total_bank += 150  # Добавляем информацию о суммарном заработке за год
        print(f"{self.name} working. Money in box + 150 ")

    def gaming(self):
        self.fullness -= 10
        self.happiness_level += 20
        print(f"{self.name} playing WOT. Happiness + 20 ")

    def pet_the_cat(self):
        self.fullness -= 10
        self.happiness_level += 5
        print(f"{self.name} petting the cat ")


class Wife(Being):
    """Создаем объект: жена"""

    def __init__(self, name, home):
        super().__init__(name=name, home=home)
        self.happiness_level = 100
        self.fur_coat_collection = 0  # Коллекция шуб жены. Для подсчета суммы купленных шуб.

    def __str__(self):
        return f"Жена. {super().__str__()}, happiness level: {self.happiness_level}"

    def is_alive(self):
        return super().is_alive() and self.happiness_level > 10

    def act(self):
        if self.home.dust_amt >= 90:
            self.happiness_level -= 10  # Проверяем насколько грязно дома

        if self.fullness <= 20:
            self.eat()
        elif self.happiness_level <= 20 and self.home.money > 350:
            self.buy_fur_coat()
        elif self.happiness_level <= 20:
            self.pet_the_cat()
        elif self.home.fridge < 60:
            self.shopping()
        elif self.home.cat_food < 20:
            self.buy_cat_food()
        else:
            self.clean_house()

    def shopping(self):
        self.fullness -= 10
        food_pay = min(60, self.home.money)
        self.home.fridge += food_pay
        self.home.money -= food_pay
        print(f"{self.name} shopping. Food in fridge + {food_pay}")

    def buy_cat_food(self):
        self.fullness -= 10
        food_pay = min(20, self.home.money)
        self.home.cat_food += food_pay
        self.home.money -= food_pay
        print(f"{self.name} buy cat food. Cat food + {food_pay}")

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

    def pet_the_cat(self):
        self.fullness -= 10
        self.happiness_level += 5
        print(f"{self.name} petting the cat ")

# TODO: мужу с женой, да и ребенку, пригодился бы класс Человек.


class Cat(Being):

    def __str__(self):
        return f"Кот. {super().__str__()}"

    def act(self):
        if self.fullness <= 10:
            self.eat()
        elif self.home.cat_food < 20:  # Была идея сделать через рандом, но решил, что это больше моделирует реальную
            self.soil()  # ситуацию. Мол мало еды - кот беснуется и дерет обои.     # TODO: норм)
        else:
            self.sleep()

    # Хотел дополнить eat в классе Being, но решил, что усложняет код. Решил переопределить.
    # TODO: а как бы ты его дополнил? через тип объекта проверял бы кто вызвал eat, чтобы отнимать от нужного поля?
    def eat(self):
        portion = min(10, self.home.cat_food)
        self.fullness += portion * 2
        self.home.cat_food -= portion
        print(f"{self.name} eating. Fullness + {portion * 2}")

    def soil(self):
        print(f"{self.name} tears wallpaper")
        self.fullness -= 10
        self.home.dust_amt += 5

    def sleep(self):
        print(f"{self.name} sleeping")
        self.fullness -= 10


class Child(Being):

    happiness_level = 100

    def __str__(self):
        return f"{super().__str__()}, happiness_level = 100"

    def act(self):
        if self.fullness <= 20:
            self.eat()
        elif random.randint(1, 2) == 1:
            self.pet_the_cat()
        else:
            self.sleep()

    # TODO: Отличается от Мужа и Жены одной цифрой.
    def eat(self):
        portion = min(10, self.home.fridge)
        self.fullness += portion
        self.home.fridge -= portion
        print(f"{self.name} eating. Fullness + {portion}")

    def sleep(self):
        self.fullness -= 10
        print(f"{self.name} sleeping")

    def pet_the_cat(self):
        self.fullness -= 10
        print(f"{self.name} petting the cat ")

# TODO: Общий класс с Child.
#  Надо изменить Родительский класс, и лучше сделать его Human, таким образом, чтобы его конструктор принимал
#  параметр "прожорливость", т.о. мы будем иметь возможность установить максимальной размер съедаемой за раз порции.
#  Внутри же конструкторов Муж/Жена/Ребенок, когда мы будем вызывать super() класса-Родителя, у нас будет жестко,
#  числом, задаваться параметр "прожорливости".
#  .
#  Т.о. конструктор: РодительскиКласс(..., прожоливость). А классы-наследники такого параметра не имеют.
#  .
#  В итоге, метод eat() будет только у Родительского класса. Этот метод будет использовать поле "прожорливость" у каждого объекта,
#  Все классы-наследники будут устаналивать это поле, когда будут вызывать конструктор Human в своем собственному конструкторе.
#  Обрати внимание, сделать Child(, прожорливость=100500) будет нельзя, т.к. Child не будет иметь параметра "прожорливость",
#  он будет его жестко задавать в собственном конструкторе:
#       super().__init__(..., прожоливость=10).


# TODO: Общий класс с Cat.
#  Вообще с котом мы способны на большее.
#  В классе Дом лучше вместо полей "кошачья еда" и "человеческая еда"
#  ввести поле "холодильник", которое может быть словарем с 2 ключами: "кошачья еда" и ...;
#  Так же лучше создать глобальные, вне классов, константы CAT_FOOD = 'cat_food' и ... Что будут играть роль ключей в этом
#  холодильнике. При создании объекта Cat конструктор класса будет вызывать конструктор Общего класса, который будет
#  принимать на вход "тип пищи", который кушает создаваемый объект.
#  .
#  А в методе eat() просто будет по умолчанию брать "тип пищи" из холодильника и отниматься от нужной пищи.
#  .
#  Сейчас наша главная задача при проектировании классов: сделать так, чтобы все общие части попали в классы-родителей.
#  а классы-наследники будут наследовать общий код.


# TODO: поля которые напрашиваются: размер порции, тип еды и коэф.насыщения (у кота == 2)


home1 = House()
serge = Husband(name='Сережа', home=home1)
masha = Wife(name='Маша', home=home1)
murzik = Cat(name='Мурзик', home=home1)
kolya = Child(name='Коля', home=home1)

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    home1.dust_append()

    if all([serge.is_alive(), masha.is_alive(), kolya.is_alive(), murzik.is_alive()]):
        serge.act()
        masha.act()
        murzik.act()
        kolya.act()
    else:
        print(f"Один из членов семьи умер.")
        # TODO: добавить прерывание

    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(kolya, color='cyan')
    cprint(murzik, color='cyan')

cprint(f"{serge.name} заработал {home1.total_bank} за год", color='red')
cprint(f"{masha.name} купила {masha.fur_coat_collection} шуб за год", color='red')

# Хотел пихнуть сюда all(). Не зря же ты про нее сказал.
# Но с ней питон отказался работать почему-то.

# TO DO: сказал не зря. Но тут он не нужен. При этом all работает с итерируемыми объектами (список/кортеж/слова),
#  т.е. ему нужно передать список/ ия ему не передашь.
#  if all([serge.is_alive(), masha.is_alive()]):        # но это сильно упрощает жизнь, поэтому тут не нужен.

# TO DO: еще одна хитрость.
#  "self.fullness > 0" сам по себе дает True|False. Нам не нужен if|else, можно сравнение
#  подставить сразу в return

# TO DO: упростить. if должен ичезнуть.
#  Использование super().is_alive() - хорошо!

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
# x = 100500 or 123       # 100500
# y = None or 123         # 123
# TO DO: проверь в интепрераторе вручную, чтобы запомнить.

# Проверил, даже написал ф-ию для теста
# def some(z):
#     return z > 1
#
# z = 1
#
# y = some(z) or 123
#
# print('y =', y) y = 123. Если z > 1, то y = True

# TO DO: все верно.

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
