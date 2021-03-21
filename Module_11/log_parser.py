# TODO: ну скорее parse_line, ведь он парсит строку и выдает нужные параметры
def split_line(line):
    date_tmp, time_tmp, log_tmp = line.split()
    date_tmp = date_tmp[1:]
    time_tmp = time_tmp[:5]
    return date_tmp, time_tmp, log_tmp


# TODO: даже название файла подсказывает название метода))
#  Но в целом, event_reader тоже неплохо. file_reader - слишком размыто.
def file_reader(filename):
    counter = 0

    with open(filename, 'r') as file:
        date, time, log_type = split_line(next(iter(file)))
        current_time = time

        # Этот if бесполезен по факту. Т.к. в первой строке нету 'NOK'.
        # Но я поставил, чтобы в случае, допустим, замены файла, все отработало нормально.

        # TODO: и правильно сделал. Без него это считалось бы ошибкой.
        #  Используй следующий трюк:
        #   X = 0
        #   X += True       # 1
        #   X *= False      # 0
        #  .
        #  True - это 1
        #  False - это 0.
        #  только к int приведи на всякий пожарный, для сохранения читабельности
        #  (если ни одной строки в файле кроме первой, не будет, то counter не должен быть True, он должен быть 1)

        if 'NOK' in log_type:
            counter += 1

        for line in file:
            date, time, log_type = split_line(line)

            if time != current_time:
                yield f'[{date} {current_time}] {counter}'
                counter = 0
                current_time = time

            if 'NOK' in log_type:
                counter += 1


# TO DO: подредактировал файл с эвентами. Последняя строка теряется.
# TODO: Последняя строка, Карл! 11:35!
grouped_events = file_reader(filename='events.txt')

for group_event in grouped_events:
    print(group_event)
