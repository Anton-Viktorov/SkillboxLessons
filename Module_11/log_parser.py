def format_line(line):
    d, t, l = line.split(' ')
    d = d[1:]
    t = t[:5]
    return d, t, l


def event_handler(filename):
    current_time = ''
    counter = 0
    with open(filename, 'r') as f:
        for line in f:
            date, time, log_type = format_line(line)

            if not current_time:
                current_time = time

            if time != current_time:
                yield f'[{date} {current_time}] {counter}'
                counter = 0
                current_time = time

            if 'NOK' in log_type:
                counter += 1


grouped_events = event_handler(filename='events.txt')

for group_event in grouped_events:
    print(group_event)
