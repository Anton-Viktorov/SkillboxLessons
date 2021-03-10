# from termcolor import cprint
import random

# TO DO: сделал и правильно использовал (по коду нигде нет 'cat_food' или 'human_food').
CAT_FOOD = 'cat_food'
HUMAN_FOOD = 'human_food'


class House:
    """Создаем объект: дом"""

    def __init__(self):
        self.money = 100
        self.fridge = {HUMAN_FOOD: 50, CAT_FOOD: 30}
        self.dust_amt = 0
        self.total_bank = 0  # Общий банк. Сколько всего муж заработает за год.

    def __str__(self):
        return f"House: \n Money in box: {self.money}, " \
               f"food in fridge: {self.fridge}, " \
               f"dust amount: {self.dust_amt}"

    def dust_append(self):
        self.dust_amt += 5  # Уровень грязи в доме


class Mammal:
    """Класс-родитель. Инициализирует модель чего-то живого(человека, кота и т.д.)"""

    def __init__(self, name, home, portion, food_type, food_coef, fullness=30):        # TO DO: запятая? / Случайно
        self.name = name
        self.fullness = fullness
        self.home = home
        self.portion = portion
        self.food_type = food_type
        self.food_coef = food_coef

    def __str__(self):
        return f"Name: {self.name}, fullness: {self.fullness}"  # Выводим общую информацию об объекте

    def eat(self):
        tmp_portion = min(self.portion, self.home.fridge[self.food_type])
        self.fullness += tmp_portion * self.food_coef
        self.home.fridge[self.food_type] -= tmp_portion
        # print(f"{self.name} eating. Fullness + {tmp_portion * self.food_coef}")

    def is_alive(self):
        return self.fullness > 0


class Human(Mammal):

    def __init__(self, name, home, portion):
        # TO DO: если имя параметра совпадает с именем аргумента, писать "имя_параметра=" не стоит.
        super().__init__(name, home, portion, food_type=HUMAN_FOOD, food_coef=1)
        self.happiness_level = 100

    def __str__(self):
        return f"{super().__str__()}, happiness level: {self.happiness_level}"

    def is_alive(self):
        return all([super().is_alive(), self.happiness_level > 10])

    def mood_drop(self):
        if self.home.dust_amt >= 90:
            self.happiness_level -= 10

    def pet_the_cat(self):
        self.fullness -= 10
        self.happiness_level += 5
        # print(f"{self.name} petting the cat ")


class Husband(Human):
    """Создаем объект: муж"""

    def __init__(self, name, home, salary):
        super().__init__(name, home, portion=30)
        self.salary = salary

    def __str__(self):
        return f"Муж. {super().__str__()}"

    def act(self):
        self.mood_drop()

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
        self.home.money += self.salary
        self.home.total_bank += self.salary  # Добавляем информацию о суммарном заработке за год
        # print(f"{self.name} working. Money in box + 150 ")

    def gaming(self):
        self.fullness -= 10
        self.happiness_level += 20
        # print(f"{self.name} playing WOT. Happiness + 20 ")


class Wife(Human):
    """Создаем объект: жена"""

    def __init__(self, name, home):
        super().__init__(name, home, portion=30)
        self.fur_coat_collection = 0

    def __str__(self):
        return f"Жена. {super().__str__()}"

    def act(self):
        self.mood_drop()

        if self.fullness <= 20:
            self.eat()
        elif self.happiness_level <= 20 and self.home.money > 350:
            self.buy_fur_coat()
        elif self.happiness_level <= 20:
            self.pet_the_cat()
        elif self.home.fridge[HUMAN_FOOD] < 60:
            self.shopping()
        elif self.home.fridge[CAT_FOOD] < 20:
            self.buy_cat_food()
        else:
            self.clean_house()

    def shopping(self):
        self.fullness -= 10
        food_pay = min(60, self.home.money)
        self.home.fridge[HUMAN_FOOD] += food_pay
        self.home.money -= food_pay
        # print(f"{self.name} shopping. Food in fridge + {food_pay}")

    def buy_cat_food(self):
        self.fullness -= 10
        food_pay = min(20, self.home.money)
        self.home.fridge[CAT_FOOD] += food_pay
        self.home.money -= food_pay
        # print(f"{self.name} buy cat food. Cat food + {food_pay}")

    def buy_fur_coat(self):
        self.fullness -= 10
        self.happiness_level += 60
        self.home.money -= 350
        self.fur_coat_collection += 1
        # print(f"{self.name} buys fur coat. Happiness + 60")

    def clean_house(self):
        self.fullness -= 10
        self.home.dust_amt -= min(self.home.dust_amt, 100)
        # print(f"{self.name} washes house")


class Cat(Mammal):

    def __init__(self, name, home):
        super(Cat, self).__init__(name, home, portion=10, food_coef=2, food_type=CAT_FOOD)

    def __str__(self):
        return f"Кот. {super().__str__()}"

    def act(self):
        if self.fullness <= 10:
            self.eat()
        elif self.home.fridge[self.food_type] < 20:
            self.soil()
        else:
            self.sleep()

    def soil(self):
        # print(f"{self.name} tears wallpaper")
        self.fullness -= 10
        self.home.dust_amt += 5

    def sleep(self):
        # print(f"{self.name} sleeping")
        self.fullness -= 10


class Child(Human):

    def __init__(self, name, home):
        super().__init__(name, home, portion=10)

    def __str__(self):
        return f"Ребенок. {super().__str__()}"

    # TO DO: только оно не уменьшается. Т.е. переопределения метода ниже вполне достаточно.
    def mood_drop(self):
        pass

    def act(self):
        if self.fullness <= 20:
            self.eat()
        elif random.randint(1, 2) == 1:
            self.pet_the_cat()
        else:
            self.sleep()

    def sleep(self):
        self.fullness -= 10
        # print(f"{self.name} sleeping")

    def pet_the_cat(self):
        self.fullness -= 10
        # print(f"{self.name} petting the cat ")


class Experiment:

    valid_coef = 0
    fatal_iterations = 0
    success_iterations = 0
    iterations = 0

    def __init__(self, numb_of_cats, salary, food_incidents, money_incidents):
        self.numb_of_cats = numb_of_cats
        self.salary = salary
        self.food_incidents = food_incidents
        self.money_incidents = money_incidents
        # Это проба пера. Для полной крутости можно прикрутить параметры количества жен, мужей и детей.
        # А вдруг это такая вот необычная семья) Пока сделал так.

    def family_generate(self):
        # TODO:
        #  1. ниже идут различные поля. PyCharm их подсвечивает желтой линией, потому что это нарушение стиля.
        #     Создание полей ВНЕ конструктора крайне не рекомендуется. Когда смотришь в конструктор, должно появляться
        #     полное появление о то, что это за объект;
        #  2. Поля ниже следует сделать локальными переменными. Метод family_generate генерирует семью, так пусть и
        #     возвращает эту "семью") Тут важный момент: использовать поля для передачи инаформации между методами
        #     нельзя. Почему? Потому что это приводит к раздуванию конструктора, у нас будет куча полей, каждое из
        #     которых можно было бы заменить передачей параметра и return`ом.
        #     .
        #     Поля объекта - это обязательная и неотъемлемая характеристика объекта. Например, у класса Муж, есть
        #     поле ЗП, оно его характеризует. Это важные параметр, который описывает мужа. Но вот например поля
        #     "текущая порция" у него нет, т.к. это изменяющееся значение, которое достаточно хранить в локальной
        #     переменной.
        #     .
        #     Текущий объект Эксперимент то же самое: у эксперимента есть параметры, условно 1 жена, 1 муж ...,
        #     но непосредственно параметров Мужья, Жены... у него нет. Для эксперимента они локальные переменные
        #     которые он создает, использует, а потом благополучно забывает о них.
        self.home = House()

        # Family
        self.family = []

        # Wife and Husband
        self.wife = Wife(name='wife', home=self.home)
        self.husband = Husband(name='husband', home=self.home, salary=self.salary)

        # Children
        self.child =Child(name='child', home=self.home)

        # Cat generator
        self.cats = []
        for cat in range(0, self.numb_of_cats):
            self.cats.append(Cat(name=f"Кот {cat + 1}", home=self.home))

        self.family = [self.wife, self.husband, self.child]
        self.family += self.cats

    def __lt__(self, other):
        # TODO: valid_coef это поле класса. Чем поле класса отличается от поля объекта?
        return self.valid_coef < other.valid_coef

    def __str__(self):
        return f"Number of cats: {self.numb_of_cats}, " \
               f"food incidents: {self.food_incidents}, " \
               f"money incidents: {self.money_incidents}, " \
               f"Salary: {self.salary}. " \
               f"Valid coefficient: {self.valid_coef}."

    def food_steal(self):
        # TODO: можно использовать //= (это не ошибка, и не ворнинг, лишь доп.инфа, позволит писать чуть короче)
        self.home.fridge[HUMAN_FOOD] = self.home.fridge[HUMAN_FOOD] // 2

    def money_steal(self):
        # TODO: тоже
        self.home.money = self.home.money // 2

    def family_alive(self):
        for x in self.family:
            # TODO: почему PYCharm подчеркивает строку ниже? что не так?
            if x.is_alive() != True:
                return False
        return True

    def simulate(self, iterations):
        self.iterations = iterations

        # TODO: неплохо. Давай познакомимся с sample.
        j = 1
        k = 1
        # TODO: Пример работы sample()
        #       random.sample(list(range(100500)), 7)		# вернет список из 7 рандомных чисел из 100500 чисел
        #  .
        #  Соответственно, берем "self.food_incidents" и получаем столько рандомных дней из 365.
        #  Чем больше стандартных функций ты будешь знать и использовать, тем короче твой код. Т.е. не изобретаешь
        #  велосипед (нет, сейчас мы его не изобретали, я в общем). На собесе, когда видят, что ты знаешь sample,
        #  zip, all, any, enumerate, filter (хотя спиское включение быстрее) или map - это играет за тебя.
        #  Совсем новички и стажеры их не используют, они для них темный лес, и они предпочитают писать свои функции.

        # TODO: переменная iteration не используется. Значит ее стоит заменить на "_", это явное указание "переменная
        #  не важна, важен только цикл".
        for iteration in range(0, iterations):
            self.family_generate()
            for day in range(365):
                if random.randint(1, 5) == 3 and j <= self.food_incidents:
                    j += 1
                    self.food_steal()
                if random.randint(1, 5) == 3 and k <= self.money_incidents:
                    k += 1
                    self.money_steal()

                # TODO: подумай как код ниже можно избавить от вложенности.
                if self.family_alive():
                    for x in self.family:
                        x.act()
                else:
                    self.fatal_iterations += 1
                    break
                # TODO: давай запустим цикл по кортежу из всех участников. И для каждого будем вызывать: act(),
                #  is_alive (можно еще и cprint()). При этом будет удобно ввести флаг f_success = True. А после каждого
                #  act() выполнять "f_success &= ...".
                #  Тогда мы сможем использовать флаг f_success чтобы прервать основной цикл, если кто-то же умрет.

        self.success_iterations = self.iterations - self.fatal_iterations

        self.valid()

    def valid(self):
        self.valid_coef = (self.success_iterations / self.iterations) * \
                          ((self.food_incidents / 5) * (self.money_incidents / 5) *
                           ((2 * 30) + (1 * 10) + (self.numb_of_cats * 10))) / self.salary

    # TODO: Поле же не скрыто. Зачем нам вызывать метод self.get_valid, если есть self.valid_coef?
    def get_valid(self):
        return self.valid_coef


results = []

for numb_of_cats in range(6):
    for food_incidents in range(6):
        for money_incidents in range(6):
            for salary in range(50, 401, 50):
                experiment = Experiment(numb_of_cats, salary, food_incidents, money_incidents)
                experiment.simulate(iterations=5)
                # TODO: пусть будут все эксперименты
                if experiment.valid_coef > 0:  # Отсекаем неудачные эксперименты, где семья не выжила.
                    results.append(experiment)

results.sort(reverse=True)

# TODO: выведи топ-5 лучших (срезы!)
for result in results:
    print(result)

# TODO: выведи топ-5 худших


# TODO: Как избавиться от лишних print`ов?
#  Мы можем закомментировать все вызовы print() и переделать много кода, чтобы не было так много выводов, а можем поступить иначе.
#  Как можно решить эту проблему аккуратно, не перепахивая сотни строк кода?
#       verbose = False             # глобальный флаг "печатать или нет"
#       native_print = print        # запоминаем исходную функцию print
#  .
#  .
#       def print(*args, **kwargs):                 # перегружаем функцию print() своей собственной
#           if verbose:                             #
#               native_print(*args, **kwargs).      # вызываем исходных print(), если глобальный флаг разрешает печать.
#  .
#  А там, где нужно напечатать всегда, независимо от флага verbose, используем native_print.
#  p.s. сначал переопределяет print, потом определяем классы, которые используют native_print.


# experiment = Experiment(numb_of_cats=3, food_incidents=2, money_incidents=2, salary=150)
# experiment.simulate(iterations=5)
#
# print(experiment)

# experiment = Experiment(numb_of_cats=3, salary=100, food_incidents=3, money_incidents=4)
# experiment.simulate(iterations=5)
# experiment.get_valid()
# print(experiment)
# print(experiment.fatal_iterations, experiment.success_iterations, experiment.iterations)

# home1 = House()
# serge = Husband(name='Сережа', home=home1)
# masha = Wife(name='Маша', home=home1)
# murzik = Cat(name='Мурзик', home=home1)
# kolya = Child(name='Коля', home=home1)
#
# family = [serge, masha, murzik, kolya]
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#
#     home1.dust_append()
#
#     if all([serge.is_alive(), masha.is_alive, kolya.is_alive(), murzik.is_alive()]):
#         for x in family:
#             x.act()
#     else:
#         print(f"Один из членов семьи умер.")
#         break
#
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')
#
# cprint(f"{serge.name} заработал {home1.total_bank} за год", color='red')
# cprint(f"{masha.name} купила {masha.fur_coat_collection} шуб за год", color='red')

# TODO: Класс Эксперимент.
#  Сделай небольшой класс Experiment.
#  В конструкторе будут все поля: число людей, кошек, ЗП, частота пропадания еды и денег, число повторений эксперимента,
#  число удачных повторений.
#  Так же нужно будет перегрузить оператор сравнения - __lt__.
#  Примечание: "__lt__" - метод вызывается при использовании оператора "<".
#  Например:   "exp_1 < exp_2" по факту вызовет следующее "Experiment.__lt__(exp_1, exp_2)". Должно возвращать
#  True или False.
#  .
#  Запускаем несколько вложенных циклов (по ЗП, кол-во кошек и т.п.), перебираем разные наборы
#  параметров. Проводим симуляции, результаты сохраняем в объекты Experiment().
#  Все результаты сохраняются в список Experiment`ов.
#  Перегрузка оператора __lt__ позволит нам отсортировать список стандартной функцией
#  sorted(my_list) и взять срез лучших и худших 5 примеров.
#  .
#  Далее, перегрузив метод __str__ у Experiment мы сможем печатать информацию об экспериментах в цикле, не
#  зная ничего о его полях, логика будет инкапсулировано в класс Эксперимент. Т.е. 1 раз написали, а дальше
#  используем, и не приходится каждый раз вспоминать, какое поле должно быть больше, меньше или
#  равно нулю.
#  .
#  p.s. так же можно добавить поле "число повторений". Чем больше повторений, тем более
#  достоверны результаты эксперимента.

# TODO: Коэффициент. Вес эксперимента.
#  У класса Experiment нужно добавить ф-цию "отдай вес". Вес эксперимента, т.е. насколько он,
#  скажем так, "крут" (т.е. эксперимент с 1 человеком, ЗП 10000, и 0 котами нас не слишком
#  интересует, поэтому его вес должен быть низкий; а вот случай, где 3 человека и 4 кота
#  выживают на 200 рублей - для нас интересен (конечно, если он успешен)).
#  .
#  Это нам пригодится для сравнения Экспериментов между собой. Мы можем ввести "веса" и сранивать этим результат, и
#  определить какой наиболее сторгий набор параметров позволит нам прокормить как можно больше котов.
#  .
#  Пример как посчитать вес:
#     вес_эксперимента = (число_успешных_попыток_эксперимента / (общее_число попыток + 3))
#                        * (число_пропаж_еды / 5)
#                        * (число_пропаж_денег / 7)
#                        * (число_человек * 30 + число_котов * 20) / ЗП
#  Посчитанный вес будет отражать ценность данного эксперимента. И будет учитывать все параметры.
#  Я написал приблизительную формулу. Вероятно, ты можешь ее уточнить, т.к. например понимаешь,
#  что какой-то из параметров доментирует над другими.
#  .
#  Наша задача: определить эксперитмен, отражающий самый-самый экстремальный способ выживания семьи.
#  .
#  Основной плюс: мы используем средства питона,
#  1. перегрузив __lt__ может использовать sort() + срезы для получения лучших/худших;
#  2. перегрузив __str__ можем получать инфу об эксперименте не вдаваясь в то, какие поля у эксперимента.

# TODO:
#  В итоге должен получится приблизительно такой код экспериментов.
#     for food_incidents in range(6):
#       for money_incidents in range(6):
#         for salary in range(50, 401, 50):
#           experiment = Experiment(salary, numb_of_cats, money_incidents, food_incidents)
#           experiment.simulate(n=5)        # 5 попыток
#           results.append(experiment)

# TO DO: этот метод трогать не надо. У ребенка есть счастье.
#  p.s. чисто логически, верно. Но с практической точки зрения - это доп.код, который можно было не делать.
#  Иначе есть опасность начать писать большие и раздутые классы. Конечно с другой стороны, такая перегрузка
#  гарантирует, что от несчастья он не умрет. Но с другой стороны, для управления счастьем мы создали метод
#  mood_drop. Можно было бы его назвать "def decrease_happiness(lvl=10)", по умолчанию убирал бы по 10 единиц.
# def is_alive(self):
#     return self.fullness > 0

# TO DO: не не не не!!!
#  класс Being, или если отталкиваться к биологии, то лучше Mammal - это был общий родитель для Кота и Человека.
#  А теперь кот наследуется от Человека. Наверное самого смутил этот момент?
#  .
#  Трушно так: у нас есть общий предок, допустим Mammal (отсылка к биологии, но если больше нравится - Being),
#  от него наследуются Кот и Человек. Все что общее между котом и человеком уходит в Mammal. У Mammal нет счастья,
#  но есть например понятие "сытость" и "есть" (и не только, подумай). Но класс не шибко большой.
#  .
#  Потом от него Cat и Human...

# TO DO: тут я отправлю аудио (это не совсем кошерно если смотреть на самые высокие каноны, но
#  если исходить из пратичности - это умеренное зло. В аудио подробнее).

# TO DO: вот оно счастье. Дублируется.

# TO DO: вариант ниже был хорош, потому что использовал "super().is_alive()":
#           return super().is_alive() and self.happiness_level > 10
#  Если способ изменения сытости изменится, то метод выше менять не надо, а текущая версия потребует пройти
#  по коду и позаменять "self.fullness > 0" на что-то другое.
#  .
#  А если еще и сделать правку с уровнем счастья, то у нас is_alive станет общим для всех людей.
#  Тоже профит..

# TO DO: такое же поле у Жены. И у Ребенка.
#  В целом то, что у Ребенка сделал поле класса - неплохой ход. Но лично я бы выбрал сделать happiness_level
#  полем для всех Human. Ну потому что это их характеристика, понимаешь? У нас может появиться класс Подросток,
#  или Бабушка/Дедушка, и у каждого будет поле "уровень счастья". Поэтому, раз оно у всех, я бы его вынес
#  в родителя. При этом, если у нас есть необходимость снижать счастье, можно сделать у родителя метод
#  "уменьшить_счастье(количество)", а у Ребенка этот метод перегрузить, чтобы для него уменьшение счастья не
#  работало вовсе. Получится, если потребуется добавить еще какой-то вид Человеков, то у них по умолчанию
#  будет и счастья и метод по его уменьшению, который можно перегрузить, настроив по своему.

# TO DO: добавить прерывание

# Хотел дополнить eat в классе Being, но решил, что усложняет код. Решил переопределить.
# TO DO: а как бы ты его дополнил? через тип объекта проверял бы кто вызвал eat, чтобы отнимать от нужного поля?
# Ну да. Изначально хотел через isinstance, но ты же сказал, что это моветон. Поэтому я сделал отдельный метод.

# TO DO: Общий класс с Child.
#  Надо изменить Родительский класс, и лучше сделать его Human, таким образом, чтобы его конструктор принимал
#  параметр "прожорливость", т.о. мы будем иметь возможность установить максимальной размер съедаемой за раз порции.
#  Внутри же конструкторов Муж/Жена/Ребенок, когда мы будем вызывать super() класса-Родителя, у нас будет жестко,
#  числом, задаваться параметр "прожорливости".
#  .
#  Т.о. конструктор: РодительскиКласс(..., прожоливость). А классы-наследники такого параметра не имеют.
#  .
#  В итоге, метод eat() будет только у Родительского класса. Этот метод будет использовать поле "прожорливость"
#  у каждого объекта,
#  Все классы-наследники будут устаналивать это поле, когда будут вызывать конструктор Human в своем собственному
#  конструкторе.
#  Обрати внимание, сделать Child(, прожорливость=100500) будет нельзя, т.к. Child не будет иметь параметра
#  "прожорливость",
#  он будет его жестко задавать в собственном конструкторе:
#       super().__init__(..., прожоливость=10).


# TO DO: Общий класс с Cat.
#  Вообще с котом мы способны на большее.
#  В классе Дом лучше вместо полей "кошачья еда" и "человеческая еда"
#  ввести поле "холодильник", которое может быть словарем с 2 ключами: "кошачья еда" и ...;
#  Так же лучше создать глобальные, вне классов, константы CAT_FOOD = 'cat_food' и ... Что будут играть роль ключей
#  в этом
#  холодильнике. При создании объекта Cat конструктор класса будет вызывать конструктор Общего класса, который будет
#  принимать на вход "тип пищи", который кушает создаваемый объект.
#  .
#  А в методе eat() просто будет по умолчанию брать "тип пищи" из холодильника и отниматься от нужной пищи.
#  .
#  Сейчас наша главная задача при проектировании классов: сделать так, чтобы все общие части попали в классы-родителей.
#  а классы-наследники будут наследовать общий код.


# TODO: поля которые напрашиваются: размер порции, тип еды и коэф.насыщения (у кота == 2)

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
