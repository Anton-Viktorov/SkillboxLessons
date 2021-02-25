from termcolor import cprint


class House:
    """Создаем объект: дом"""

    def __init__(self):
        self.money_in_box = 100
        self.food_in_fridge = 50
        self.dust_amount = 0
        self.total_bank = 0  # Общий банк. Сколько всего муж заработает за год.

    def __str__(self):
        return f"House: \n Money in box: {self.money_in_box}, " \
               f"food in fridge: {self.food_in_fridge}, " \
               f"dust amount: {self.dust_amount}"

    def dust_append(self):
        self.dust_amount += 5    # Уровень грязи в доме


class Being:
    """Класс-родитель. Инициализирует модель чего-то живого(человека, кота и т.д.)"""

    def __init__(self, name, fullness=30, happiness_level=100):
        self.name = name
        self.fullness = fullness
        self.happiness_level = happiness_level

    def __str__(self):
        return f"Name: {self.name}, fullness: {self.fullness}, " \
               f"Happiness level: {self.happiness_level}"    # Выводим общую информацию об объекте


class Husband(Being):
    """Создаем объект: муж"""

    def __init__(self, name):
        super().__init__(name=name)
        self.role = 'Муж'  # Определяем роль в семье

    def __str__(self):
        result = super().__str__()
        return f"{self.role}. {result}"  # Суммируем результаты с классом Being

    def act(self):
        if home.dust_amount >= 90:
            self.happiness_level -= 10  # Проверяем насколько грязно дома

        if self.fullness <= 0 or self.happiness_level <= 10:
            print(f"{self.name} умер")

        if self.fullness <= 10:
            self.eat()
        elif self.happiness_level <= 10:
            self.gaming()
        else:
            self.work()

    def eat(self):
        if home.food_in_fridge < 30:  # Проверяем хватит ли еды в холодильнике для полного насыщения
            print(f"{self.name} eating. Fullness + {home.food_in_fridge} ")
            self.fullness += home.food_in_fridge
            home.food_in_fridge = 0
        else:
            self.fullness += 30
            home.food_in_fridge -= 30
            print(f"{self.name} eating. Fullness + 30")

    def work(self):
        self.fullness -= 10
        print(f"{self.name} working. Money in box + 150 ")
        home.money_in_box += 150
        home.total_bank += 150  # Добавляем информацию о суммарном заработке за год

    def gaming(self):
        self.fullness -= 10
        print(f"{self.name} playing WOT. Happiness + 20 ")
        self.happiness_level += 20


class Wife(Being):
    """Создаем объект: жена"""

    def __init__(self, name):
        super().__init__(name=name)
        self.role = 'Жена'
        self.fur_coat_collection = 0  # Коллекция шуб жены. Для подсчета суммы купленных шуб.

    def __str__(self):
        result = super().__str__()
        return f"{self.role}. {result}"

    def act(self):
        if home.dust_amount >= 90:
            self.happiness_level -= 10  # Проверяем насколько грязно дома

        if self.fullness <= 0 or self.happiness_level <= 10:
            print(f"{self.name} умерла")

        if self.fullness <= 10:
            self.eat()
        elif self.happiness_level <= 10 and home.money_in_box > 350:
            self.buy_fur_coat()
        elif home.food_in_fridge < 60:
            self.shopping()
        else:
            self.clean_house()

    def eat(self):
        if home.food_in_fridge < 30:  # Проверяем хватит ли еды в холодильнике для полного насыщения
            print(f"{self.name} eating. Fullness + {home.food_in_fridge}")
            self.fullness += home.food_in_fridge
            home.food_in_fridge = 0
        else:
            self.fullness += 30
            home.food_in_fridge -= 30
            print(f"{self.name} eating. Fullness + 30 ")

    def shopping(self):
        self.fullness -= 10
        if home.money_in_box > 120:  # Если денег достаточно много, то закупаем еды на 2 приема пищи
            home.money_in_box -= 60
            home.food_in_fridge += 60
            print(f"{self.name} shopping. Food in fridge + 60 ")
        else:
            print(f"{self.name} shopping. Food in fridge + {home.money_in_box} ")
            home.food_in_fridge += home.money_in_box
            home.money_in_box = 0

    def buy_fur_coat(self):
        self.fullness -= 10
        print(f"{self.name} buys fur coat. Happiness + 60")
        self.happiness_level += 60
        home.money_in_box -= 350
        self.fur_coat_collection += 1

    def clean_house(self):
        self.fullness -= 10
        print(f"{self.name} washes house")
        if home.dust_amount > 100:  # Проверяем, сможет ли жена убрать всю грязь в доме за 1 раз
            home.dust_amount -= 100
        else:
            home.dust_amount = 0


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    home.dust_append()
    serge.act()
    masha.act()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')

cprint(f"{serge.name} заработал {home.total_bank} за год", color='red')
cprint(f"{masha.name} купила {masha.fur_coat_collection} шуб за год", color='red')
