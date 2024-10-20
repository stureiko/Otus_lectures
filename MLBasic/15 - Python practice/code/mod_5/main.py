# модуль, реализующий интерфейс командной строки, 
# позволяющий на основе передаваемых параметров выполнять предсказание значений по исходным данным;
# написание тестов.

import argparse
from model import Model
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика для logger2
file_handler = logging.FileHandler(f"{__name__}.log", mode='w')
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
file_handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def parse_args():
    logger.info('Parse arguments')
    parser = argparse.ArgumentParser(description='My ml module')
    parser.add_argument('val_list', nargs='+', default=[1., 3.], type=float, help='Required list of values')

    parser.add_argument('-m_1',
                        '--my_optional_1',
                        type=int,
                        default=2,
                        help='provide an integer (default: 2)'
    )

    parser.add_argument('-l','--list', nargs='+', default=[1, 3], type=int, help='<Required> Set flag', required=False)
    try:
        args = parser.parse_args()
    except Exception as e:
        logger.error(e)
    return args    

def main():
    logger.info('Start main()')
    try:
        args = parse_args()
    except Exception as e:
        logger.error(e)

    print(args.val_list)
    logger.info('Create model')
    model = Model()

    try:
        res, idx = model.predict(args.val_list)
    except Exception as e:
        logger.error(e)

    if res:
        print('All elements are great than zero')
    else:
        print(f'The elements {idx} less than zero')


if __name__ == '__main__':
    main()