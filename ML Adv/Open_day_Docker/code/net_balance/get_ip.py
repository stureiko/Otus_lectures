from netifaces import interfaces, ifaddresses, AF_INET

def main():
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        if addresses != ['No IP addr']:
            print(ifaceName, ', '.join(addresses))

if __name__ == '__main__':
    main()