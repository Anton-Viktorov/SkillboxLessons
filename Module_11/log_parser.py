
# TO DO: как функцию лучше назвать? что он делает?
def split_line(line):
    # TO DO: фффф. Ну и нейминг. Что за переменные курильщика? Пожадничал букв?
    #  1. поправить имена; читабельность пострадала и не уверен, что оправится;
    #  2. в split по умолчанию " ", поэтому обычно не подставляют.
    date_tmp, time_tmp, log_tmp = line.split()
    date_tmp = date_tmp[1:]
    time_tmp = time_tmp[:5]
    return date_tmp, time_tmp, log_tmp


# TO DO: что делает эта функция? она не обработчик событий.
#  Да, с точки зрения английкого - путем. Но хендлерами принято называть функции/методы, которые срабатывают на какое-
#  то событие. Например, в телеграмм боте ты писал хендлеры сообщений.
#  .
#  Это не хендлер. Принимает на вход имя файла, что-то с ним делает... что делает эта функция?
def file_reader(filename):
    # TO DO: это переменные здорого человека.
    counter = 0

    # TO DO: лучше "file", чаще видел именно как file. f - режет глаз.
    with open(filename, 'r') as file:
        # TO DO: line - верно.
        date, time, log_type = split_line(next(iter(file)))
        current_time = time

        # Ещё вариант.
        # date, time, log_type = split_line(file.readline())
        # current_time = time

        # Этот if бесполезен по факту. Т.к. в первой строке нету 'NOK'.
        # Но я поставил, чтобы в случае, допустим, замены файла, все отработало нормально.

        if 'NOK' in log_type:
            counter += 1

        for line in file:
            # TO DO: вооо, норм нейминг. А в функции какой-то треш
            date, time, log_type = split_line(line)

            # TO DO: if ниже нужен, чтобы инициализировать первым значением current_time.
            #  Как это можно сделать снаружи, не запуская цикл? (вспомни про next()!).

            if time != current_time:
                yield f'[{date} {current_time}] {counter}'
                counter = 0
                current_time = time

            if 'NOK' in log_type:
                counter += 1


# TO DO: подредактировал файл с эвентами. Последняя строка теряется.
grouped_events = file_reader(filename='events.txt')

for group_event in grouped_events:
    print(group_event)
