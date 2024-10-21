# модуль, реализующий интерфейс командной строки, 
# позволяющий на основе передаваемых параметров выполнять предсказание значений по исходным данным;
# написание тестов.

import argparse
from model import Model

def parse_args():
    parser = argparse.ArgumentParser(description='My ml module')
    # parser.add_argument('val_list', nargs='+', default=[1., 3.], type=float, help='Required list of values')

    parser.add_argument('-m_1',
                        '--my_optional_1',
                        type=int,
                        default=2,
                        help='provide an integer (default: 2)'
    )

    parser.add_argument('-l','--list', nargs='+', default=[1, 3], type=float, help='<Required> Set flag', required=False)

    args = parser.parse_args()
    return args    

def main():
    args = parse_args()
    print(args.list)
    model = Model()

    res, idx = model.predict(args.list)

    if res:
        print('All elements are great than zero')
    else:
        print(f'The elements {idx} less than zero')


if __name__ == '__main__':
    main()