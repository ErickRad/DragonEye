import backend

if __name__ == '__main__':
    while True:
        option = int(input('''
-------------------- DRAGON EYE ---------------------

1 - Verify your network connection
2 - Check devices on your network
3 - Perform a network speed test
4 - Exit

Choose an option: '''))

        match option:
            case 1:
                print(backend.isConnected())
            case 2:
                if backend.isConnected():
                    devices = backend.scanDevices()
                    for device in devices:
                        print(f"IP: {device[0]}       MAC: {device[1]}       Brand: {device[2]}")
                    devices = None
            case 3:
                print(backend.checkInternetSpeed())
            case _:
                break

