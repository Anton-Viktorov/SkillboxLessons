
# TODO: как функцию лучше назвать? что он делает?
def format_line(line):
    # TODO: фффф. Ну и нейминг. Что за переменные курильщика? Пожадничал букв?
    #  1. поправить имена; читабельность пострадала и не уверен, что оправится;
    #  2. в split по умолчанию " ", поэтому обычно не подставляют.
    d, t, l = line.split(' ')
    d = d[1:]
    t = t[:5]
    return d, t, l


# TODO: что делает эта функция? она не обработчик событий.
#  Да, с точки зрения английкого - путем. Но хендлерами принято называть функции/методы, которые срабатывают на какое-
#  то событие. Например, в телеграмм боте ты писал хендлеры сообщений.
#  .
#  Это не хендлер. Принимает на вход имя файла, что-то с ним делает... что делает эта функция?
def event_handler(filename):
    # TODO: это переменные здорого человека.
    current_time = ''
    counter = 0

    # TODO: лучше "file", чаще видел именно как file. f - режет глаз.
    with open(filename, 'r') as f:
        # TODO: line - верно.
        for line in f:
            # TODO: вооо, норм нейминг. А в функцие какой-то треш
            date, time, log_type = format_line(line)

            # TODO: if ниже нужен, чтобы инициализировать первым значением current_time.
            #  Как это можно сделать снаружи, не запуская цикл? (вспомни про next()!).
            if not current_time:
                current_time = time

            if time != current_time:
                yield f'[{date} {current_time}] {counter}'
                counter = 0
                current_time = time

            if 'NOK' in log_type:
                counter += 1


# TODO: подредактировал файл с эвентами. Последняя строка теряется.
grouped_events = event_handler(filename='events.txt')

for group_event in grouped_events:
    print(group_event)
