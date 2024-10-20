def parse_user_data(data):
    print(f'parsing: {data}')


if __name__ == '__main__':
    import sys

    print(sys.argv)

    if len(sys.argv) > 1:
        parse_user_data(sys.argv[1])

    # print(__file__)
    # print(__name__)
    # parse_user_data('test data')
