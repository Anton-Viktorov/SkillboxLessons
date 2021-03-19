import logging


def log_errors(f_name):
    def create_logger(fun):
        logger = logging.getLogger(f"function: {fun.__name__}")
        logger.setLevel(logging.ERROR)

        logger_handler = logging.FileHandler(f_name)
        logger.setLevel(logging.ERROR)

        logging_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        logger_handler.setFormatter(logging_formatter)

        logger.addHandler(logger_handler)

        def inner(*args, **kwargs):
            try:
                # TODO: сразу можно return, без result
                result = fun(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                # TODO: кое-чего стер. Оставил только raise. В таком случае будет возбуждено исключение, которое
                #  было последним.
                raise
            return result

        return inner

    return create_logger


@log_errors(f_name='function_errors.log')
def perky(param):
    return param / 0


@log_errors(f_name='function_errors.log')
def check_line(line):
    name, email, age = line.split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not a email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]

for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')

try:
    perky(param=42)
except ZeroDivisionError as e:
    print(e)
