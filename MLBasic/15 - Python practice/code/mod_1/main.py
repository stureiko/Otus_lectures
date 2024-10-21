# модуль, реализующий интерфейс командной строки, 
# позволяющий на основе передаваемых параметров выполнять предсказание значений по исходным данным;
# написание тестов.

import argparse

def model(val: list) -> tuple[bool, tuple[int]]:
    # check all elements in list are great than zero
    res = all(v >= 0 for v in val)
    if res:
        idx = []
    else:
        idx = [index for index, value in enumerate(val) if value < 0]
    return (res, idx)

def main():
    parser = argparse.ArgumentParser(description='My ml module')
    # parser.add_argument('val_list', nargs='*', default=[1., 3.], type=float, help='Required list of values')

    parser.add_argument('-m_1',
                        '--my_optional_1',
                        type=int,
                        default=2,
                        help='provide an integer (default: 2)'
    )

    parser.add_argument('-l','--list', nargs='+', default=[1, 3], type=float, help='<Required> Set flag', required=False)

    args = parser.parse_args()
    print(args)
    
    res, idx = model(args.list)

    if res:
        print('All elements are great than zero')
    else:
        print(f'The elements {idx} less than zero')


if __name__ == '__main__':
    main()
