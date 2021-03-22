# TO DO: ну скорее parse_line, ведь он парсит строку и выдает нужные параметры
def parse_line(line):
    date_tmp, time_tmp, log_tmp = line.split()
    date_tmp = date_tmp[1:]
    time_tmp = time_tmp[:5]
    return date_tmp, time_tmp, log_tmp


# TO DO: даже название файла подсказывает название метода))
#  Но в целом, event_reader тоже неплохо. file_reader - слишком размыто.
def event_reader(filename):
    counter = 0

    with open(filename, 'r') as file:
        date, time, log_type = parse_line(next(iter(file)))
        current_time = time

        # Этот if бесполезен по факту. Т.к. в первой строке нету 'NOK'.
        # Но я поставил, чтобы в случае, допустим, замены файла, все отработало нормально.

        # TO DO: и правильно сделал. Без него это считалось бы ошибкой.
        #  Используй следующий трюк:
        #   X = 0
        #   X += True       # 1
        #   X *= False      # 0
        #  .
        #  True - это 1
        #  False - это 0.
        #  только к int приведи на всякий пожарный, для сохранения читабельности
        #  (если ни одной строки в файле кроме первой, не будет, то counter не должен быть True, он должен быть 1)

        # Надеюсь я правильно тебя понял. А то моя конструкция меня озадачила.

        counter += int('NOK' in log_type)

        # TO DO: 'NOK' in log_type дает True или False сам по себе.

        for line in file:

            date, time, log_type = parse_line(line)

            if time != current_time:
                yield f'[{date} {current_time}] {counter}'
                counter = 0
                current_time = time

            counter += int('NOK' in log_type)

        yield f'[{date} {current_time}] {counter}'

# TO DO: подредактировал файл с эвентами. Последняя строка теряется.
# TO DO: Последняя строка, Карл! 11:35!
# Сори, сначала не понял в чем заключается to do. Думал это просто инфа к сведению. Поправил.


grouped_events = event_reader(filename='events.txt')

for group_event in grouped_events:
    print(group_event)
